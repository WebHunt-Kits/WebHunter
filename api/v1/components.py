import datetime
from typing import Dict

from flask import request
from flask_mico import ApiView, validator
from flask_mico.error import AppError, NotSupportedError
from sqlalchemy import and_
from sqlalchemy import exc as sqlalchemy_exc

from core.errors import APIErrorStausCode
from core.extensions import db
from core.field_schema import COMPONENTS_GET_SCHEMA
from core.models.component import Component


def process_component_data(component: Component, ignore_cols=("_id", "deleted_at")) -> Dict:
    data = component.to_dict(ignore_cols=ignore_cols)
    data["id"] = data.pop("c_id")
    data["name"] = data.pop("c_name")
    data["first"] = data.pop("c_first")
    data["type"] = data.pop("c_type")
    return data


def get_component_from_cid(c_id: str) -> Component:
    try:
        component = Component.query.filter_by(
            c_id=c_id, deleted_at=None).first()
    except sqlalchemy_exc.SQLAlchemyError:
        raise AppError(APIErrorStausCode.DATABASE_ERR)
    if not component:
        raise NotSupportedError()
    return component


class Components(ApiView):
    @validator(COMPONENTS_GET_SCHEMA, in_params=True)
    def get(self):
        # paging
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 50))

        # filters
        components_query = [Component.deleted_at == None]
        filters = (request.args.get('name', None), request.args.get(
            "type", None), request.args.get("first", None))
        if filters[0]:
            components_query.append(
                Component.c_name.ilike("%"+filters[0]+"%"))
        if filters[1]:
            components_query.append(Component.c_type == filters[1])
        if filters[2]:
            components_query.append(Component.c_first == filters[2])

        components_paginate = Component.query.filter(
            and_(*components_query)).paginate(page=page, per_page=per_page)
        data = {
            "cur_page_num": components_paginate.page,
            "per_page_num": components_paginate.per_page,
            "total_num": components_paginate.total,
            "total_page_num": components_paginate.pages,
            "has_prev": components_paginate.has_prev,
            "has_next": components_paginate.has_next
        }
        data["components"] = []
        for c in components_paginate.items:
            data["components"].append(process_component_data(c))
        return self.on_success(data=data)


class SpecifyComponents(ApiView):

    def get(self, c_id: str):
        component = get_component_from_cid(c_id)
        data = process_component_data(component)
        return self.on_success(data=data)

    def delete(self, c_id: str):
        component = get_component_from_cid(c_id)
        component.deleted_at = datetime.datetime.now()
        db.session.commit()
        return self.on_success(data=c_id)
