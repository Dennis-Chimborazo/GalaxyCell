import json
from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib import messages
from ..services import delete_screen_inventory

class ScreenInventoryDeleteView(View):
    def post(self, request, pk, *args, **kwargs):
        try:
            # Ejecutamos el servicio de borrado usando el pk del inventario
            result = delete_screen_inventory(inventory_id=pk)
            
            if not result.get("success"):
                error_msg = result.get("error", "No se pudo eliminar el registro de inventario.")
                messages.error(request, error_msg)
                
                response = HttpResponse(status=400)
                response["HX-Trigger"] = json.dumps({
                    "refreshTable": True,
                    "close-modal": True,
                })
                return response
                
            # Si todo sale bien
            messages.success(request, "Se eliminó correctamente el registro de inventario")
            
            response = HttpResponse(status=200)
            response["HX-Trigger"] = json.dumps({
                "refreshTable": True,
                "close-modal": True,
            })
            
            return response

        except Exception as e:
            messages.error(request, f"Error inesperado al eliminar: {str(e)}")
            
            response = HttpResponse(status=500)
            response["HX-Trigger"] = json.dumps({
                "refreshTable": True,
                "close-modal": True,
            })
            
            return response