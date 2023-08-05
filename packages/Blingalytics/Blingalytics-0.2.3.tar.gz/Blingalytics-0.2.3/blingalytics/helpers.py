import csv
from cStringIO import StringIO
import json

from blingalytics import get_report_by_code_name
from blingalytics.caches import cache_connection, local_cache


# Default cache if none specified (only load sqlite3 if using it)
DEFAULT_CACHE = local_cache.LocalCache()


@cache_connection
def report_response(params, runner=None, cache=DEFAULT_CACHE):
    """
    This frontend helper function is meant to be used in your
    request-processing code to handle all AJAX responses to the Blingalytics
    JavaScript frontend.

    In its most basic usage, you just pass in the request's GET parameters
    as a ``dict``. This will run the report, if required, and then pull the
    appropriate data. It will return a tuple of three values:

    * The response body content, as a string
    * The response mimetype, as a string
    * A dict of header values to be sent in the response

    Your request-processing code should return the described response. The
    function also accepts two options:

    ``runner`` *(optional)*
        If you want your report to run asynchronously so as not to tie up
        your web server workers while processing requests, you can specify a
        runner function. This should be a function that will initiate your
        async processing on a tasks machine or wherever. It will be passed
        two arguments: the report code_name, as a string; and the remaining
        GET parameters so you can process user inputs. By default, no runner
        is used.

    ``cache`` *(optional)*
        By default, this will use a local cache stored at
        ``/tmp/blingalytics_cache``. If you would like to use a different
        cache, simply provide the cache instance.
    """
    # Find and instantitate the report class
    if hasattr(params, 'iterlists'):
        params = dict([
            (key, (values if len(values) > 1 else values[0]))
            for key, values in params.iterlists()
        ])
    params = dict((k, v) for k, v in params.items())
    report_code_name = params.pop('report', None)
    if not report_code_name:
        return (json.dumps({'errors': ['Report code name not specified.']}),
            'application/javascript', {})
    report_cls = get_report_by_code_name(report_code_name)
    if not report_cls:
        return (json.dumps({'errors': ['Specified report not found.']}),
            'application/javascript', {})
    report = report_cls(cache)

    # Return immediately for metadata request
    if params.pop('metadata', False):
        return (json.dumps({
            'errors': [],
            'widgets': report.render_widgets(),
            'header': report.report_header(),
            'default_sort': report.default_sort,
        }), 'application/javascript', {})

    # Process user inputs
    errors = report.clean_user_inputs(**params)
    if errors:
        return (json.dumps({
            'errors': [str(error) for error in errors],
        }), 'application/javascript', {})

    # Clear cache if requested
    if params.get('killcache', False):
        report.kill_cache()
        return (json.dumps({
            'errors': [],
        }), 'application/javascript', {})

    # Run the report, either synchronously or not, if needed
    if not report.is_report_finished():
        if runner:
            if not report.is_report_started():
                runner(report_code_name, params)
            return (json.dumps({
                'errors': [],
                'poll': True,
            }), 'application/javascript', {})
        else:
            report.run_report()

    # Return full report as downloadable csv if format requested
    if params.get('format') == 'csv':
        if params.get('download', False):
            output = StringIO()
            writer = csv.writer(output)
            writer.writerow([report.display_name])
            writer.writerow(['Timestamp: %s' % report.report_timestamp()
                .strftime('%m-%d-%Y %I:%M %p UTC')])
            writer.writerow([])
            header = report.report_header()
            writer.writerow(filter(
                lambda a: a is not None,
                map(
                    lambda a: a['label'] if not a.get('hidden') else None,
                    header
                )
            ))
            for row in report.report_rows(format='csv'):
                writer.writerow(map(
                    lambda a: a[1],
                    filter(lambda a: not a[0].get('hidden'), zip(header, row))
                ))
            return (output.getvalue(), 'text/csv', {
                'Content-Disposition': 'attachment; filename="%s.csv"' \
                    % report.display_name
            })
        else:
            return (json.dumps({
                'errors': [],
                'poll': False,
            }), 'application/javascript', {})

    # Return report data
    offset = int(params.get('iDisplayStart'))
    limit = int(params.get('iDisplayLength'))
    sort_col = params.get('iSortCol_0')
    if sort_col:
        sort_col = report.columns[int(sort_col) - 1][0]
    else:
        sort_col = report.default_sort[0]
    sort_dir = str(params.get('sSortDir_0', report.default_sort[1]))
    sort = (sort_col, sort_dir)
    echo = int(params.get('sEcho'))
    return (json.dumps({
        'errors': [],
        'poll': False,
        'iTotalRecords': report.report_row_count(),
        'iTotalDisplayRecords': report.report_row_count(),
        'sEcho': str(echo),
        'aaData': report.report_rows(sort=sort, limit=limit, offset=offset),
        'footer': report.report_footer(),
    }), 'application/javascript', {})
