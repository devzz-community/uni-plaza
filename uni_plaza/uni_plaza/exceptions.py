from rest_framework.views import exception_handler


def core_exception_handler(exc, context):
    # Если возникает исключение, которые не обрабатывается здесь явно,
    # передать его обработчику исключений по-умолчанию, предлагаемому
    # DRF. Если обрабатывается такой тип исключения, нужен
    # доступ к сгенерированному DRF - получим его заранее здесь.
    response = exception_handler(exc, context)
    handlers = {
        'ValidationError': _handle_generic_error
    }
    # Определить тип текущего исключения. Воспользуемся этим, чтобы
    # решить, делать ли это самостоятельно или отдать эту работу DRF.
    exception_class = exc.__class__.__name__

    if exception_class in handlers:
        # Если это исключение можно обработать - обработать, в противном
        # случае, вернуть ответ сгенерированный стандартными средствами заранее
        return handlers[exception_class](exc, context, response)

    return response


def _handle_generic_error(exc, context, response):
    # Самый простой обработчик исключений. Берем ответ
    # сгенерированный DRF и заключаем его в ключ 'errors'.
    # response.data = {
    #     'errors': response.data
    # }

    err = []
    for error in response.data:
        err.append(error)
    for e in err:
        response.data['errors'] = response.data.pop(e)

    return response
