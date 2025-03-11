from django.utils.deprecation import MiddlewareMixin

class PorcentajeMiddleware(MiddlewareMixin):
    def process_template_response(self, request, response):
        # Verificar si el usuario está autenticado
        if request.user.is_authenticated:
            # Obtener los porcentajes almacenados en la sesión (si existen)
            datos_personales_porcentaje = request.session.get('datos_personales_porcentaje', 0)
            contacto_porcentaje = request.session.get('contacto_porcentaje', 0)
            file_porcentaje = request.session.get('file_porcentaje', 0)
            porcentaje_registro = request.session.get('porcentaje_registro', 0)
            response.context_data['datos_personales_porcentaje'] = datos_personales_porcentaje
            response.context_data['contacto_porcentaje'] = contacto_porcentaje
            response.context_data['file_porcentaje'] = file_porcentaje
             
            response.context_data['porcentaje_registro'] = porcentaje_registro
        return response
