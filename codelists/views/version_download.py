from django.http import HttpResponse, HttpResponseBadRequest

from .decorators import load_version


@load_version
def version_download(request, clv):
    fixed_headers = "fixed-headers" in request.GET
    if fixed_headers and not clv.downloadable:
        return HttpResponseBadRequest("Codelist is not downloadable")
    response = HttpResponse(content_type="text/csv")
    content_disposition = 'attachment; filename="{}.csv"'.format(
        clv.download_filename()
    )
    response["Content-Disposition"] = content_disposition
    response.write(clv.csv_data_for_download(fixed_headers=fixed_headers))
    return response
