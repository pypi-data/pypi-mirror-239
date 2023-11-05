from __future__ import annotations
import logging
from typing import (
    TYPE_CHECKING,
    Any,
    Optional,
    Dict,
    List,
)

from bson.objectid import ObjectId
from mongoengine import context_managers
from stereotech_cloud_commons.components.mongo_database import Role, RoleEntity

if TYPE_CHECKING:
    from stereotech_cloud_commons.confighelper import ConfigHelper
    from stereotech_cloud_commons.websockets import WebRequest
    from stereotech_cloud_commons.components import mongo_database

    DBComp = mongo_database.MongoDatabase

INDEX_FULL_SEARCH = "text_search_index"



class Roles:
    def __init__(self, config: ConfigHelper) -> None:
        """Service for managing user roles."""
        self.server = config.get_server()
        self.entity_name = config.get('entity_name', None)
        if self.entity_name is not None:
            self.context = context_managers.switch_collection(Role, f'{self.entity_name}_roles')
        else:
            self.context = context_managers.switch_collection(Role, 'roles')

        logging.info("Roles configuration loaded.")

        self.server.register_endpoint("/roles/role", ["POST", "DELETE", "GET"],
                                      self.handle_manage_role)
        self.server.register_endpoint("/roles/list", ["GET"],
                                      self.handle_all_roles)
        self.server.register_endpoint("/roles/scopes", ["GET"],
                                      self.handle_all_scopes)

    async def handle_all_roles(self, web_request: WebRequest) -> Dict[str, Any]:
        args = web_request.get_args()
        query = Role
        count = 0
        items = []
        if self.entity_name is not None:
            entity_id = web_request.get_str(f'{self.entity_name}_id')
            with self.context as Role_ctx:
                query = Role_ctx.objects(entity__id=entity_id) # type: ignore
                count, items = query.get_items(**args) # type: ignore
        else:
            count, items = query.get_items(**args) # type: ignore
        return {"count": count, "items": items}

    async def handle_manage_role(self, web_request: WebRequest) -> Role | Dict[str,Any]:
        action = web_request.get_action()
        if self.context is not None:
            with self.context as Role:
                if action == "POST":
                    data = web_request.get_args()

                    # Update role
                    if "id" in data:
                        logging.info("Update role | id: %s.", data["id"])
                        role = self.get_role_or_404(data["id"])
                        del data["id"]
                        data.pop("entity", None)
                        role.modify(**data)
                        role.save()
                        return role

                    # Create role
                    else:
                        name = web_request.get_str('name')
                        scopes = web_request.get('scopes')
                        logging.info("Creating role | name: %s, scopes: %s.", name,
                                     scopes)

                        role = Role(name=name, scopes=scopes)
                        if self.entity_name is not None:
                             entity_id = web_request.get_str(f'{self.entity_name}_id')
                             role.entity = RoleEntity(name=self.entity_name, id=entity_id)
                        role.save()
                        return role

                elif action == "DELETE":
                    role_id: str = web_request.get_str("id")
                    logging.info("Delete role | id: %s.", role_id)
                    role_db = self.get_role_or_404(role_id)
                    role_db.delete()
                    return {"deleted": role_id}

                elif action == "GET":
                    role_id: str = web_request.get_str("id")
                    logging.info("Get role | id: %s.", role_id)
                    return self.get_role_or_404(role_id)

        raise self.server.error('Method Not Allowed', 405)

    async def handle_all_scopes(self, web_request: WebRequest) -> Dict[str, Any]:
        """Get a list of all scopes."""
        args = web_request.get_args()
        with self.context as Role:
            count, items = Role.get_scopes(**args) # type: ignore
        return {"count": count, "items": items}

    def get_role_or_404(self, role_id: str) -> Role:
        try:
            role_db = Role.get_item(role_id) # type: ignore
        except:
            raise self.server.error(f"Role {role_id} not found", 404)
        if role_db is None:
            raise self.server.error(f"Role {role_id} not found", 404)
        return role_db


def load_component(config: ConfigHelper) -> Roles:
    return Roles(config)
