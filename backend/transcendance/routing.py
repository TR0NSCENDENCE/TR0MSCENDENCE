import pong.routing
import users.routing

ws_urlpatterns = pong.routing.ws_urlpatterns + users.routing.ws_urlpatterns
