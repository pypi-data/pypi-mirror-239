import heaobject.root
from .. import response
from ..heaobjectsupport import new_heaobject_from_type, has_permissions, PermissionGroup
from .mongo import MongoContext
from heaobject.error import DeserializeException
from aiohttp.web import Request, StreamResponse, Response
from typing import Any, AsyncGenerator, Literal, Type, IO, Optional
from heaobject.root import DesktopObject, DesktopObjectDict, desktop_object_from_dict
from heaobject.user import NONE_USER
from heaserver.service.oidcclaimhdrs import SUB
from pymongo.errors import WriteError


async def get_dict(request: Request, collection: str,
                           volume_id: Optional[str] = None) -> DesktopObjectDict | None:
    """
    Gets the requested desktop object as a desktop object dict.

    :param request: the HTTP request, which must have an id value in the match_info mapping. Required.
    :param collection: the Mongo collection name. Required.
    :param volume_id: the id string of the volume containing the requested HEA
    object. If None, the root volume is assumed.
    :return: a desktop object dict or None if the object was not found.
    """
    async with MongoContext(request, volume_id) as mongo:
        result = await mongo.get(request, collection, var_parts='id',
                                sub=request.headers.get(SUB))

        if result is not None:
            obj = heaobject.root.desktop_object_from_dict(result)
            permitted = has_permissions(obj=obj, sub=request.headers.get(SUB),
                                        permissions=PermissionGroup.GETTER_PERMS.perms)
            if not permitted:
                return None

        return result


async def get(request: Request, collection: str, volume_id: Optional[str] = None) -> Response:
    """
    Gets the desktop object with the specified id. The desktop object is
    formatted according to the requested mime types in the HTTP request's
    Accept header as one of the formats supported by the
    heaserver.service.representor module.

    :param request: the HTTP request, which must have an id value in the match_info mapping. Required.
    :param collection: the Mongo collection name. Required.
    :param volume_id: the id string of the volume containing the requested HEA object. If None, the root volume is
    assumed.
    :return: a Response with the requested HEA object or Not Found.
    """
    result = await get_dict(request, collection, volume_id)
    return await response.get(request, desktop_object_from_dict(result).to_dict() if result is not None else None)


async def get_content(request: Request, collection: str, volume_id: Optional[str] = None) -> StreamResponse:
    """
    Gets the HEA object's associated content.

    :param request: the HTTP request. Required.
    :param collection: the Mongo collection name. Required.
    :param volume_id: the id string of the volume containing the requested HEA object. If None, the root volume is
    assumed.
    :return: an aiohttp StreamResponse with the requested HEA object or Not Found.
    """
    async with MongoContext(request, volume_id) as mongo:
        result = await mongo.get(request, collection, var_parts='id', sub=request.headers.get(SUB))

        if result is not None:
            obj = heaobject.root.desktop_object_from_dict(result)
            permitted = has_permissions(obj=obj, sub=request.headers.get(SUB), permissions=PermissionGroup.GETTER_PERMS.perms)
            if not permitted:
                return response.status_not_found()
        out = await mongo.get_content(request, collection, var_parts='id', sub=request.headers.get(SUB))
        if out is not None:
            return await response.get_streaming(request, out, 'text/plain')
        else:
            return response.status_not_found()


async def get_by_name(request: Request, collection: str,
                      volume_id: Optional[str] = None) -> Response:
    """
    Gets an HTTP response object with the requested desktop object in the body.
    The desktop object is formatted according to the requested mime types in
    the HTTP request's Accept header as one of the formats supported by the
    heaserver.service.representor module.

    :param request: the HTTP request, which must have a name value in the match_info mapping. Required.
    :param collection: the Mongo collection name. Required.
    :param volume_id: the id string of the volume containing the requested
    desktop object. If None, the root volume is assumed.
    :return: a Response with the requested desktop object or Not Found.
    """
    result = await get_by_name_dict(request, collection, volume_id)
    return await response.get(request, desktop_object_from_dict(result).to_dict() if result is not None else None)

async def get_by_name_dict(request: Request, collection: str,
                           volume_id: Optional[str] = None) -> DesktopObjectDict | None:
    """
    Gets the requested desktop object as a desktop object dict.

    :param request: the HTTP request, which must have a name value in the match_info mapping. Required.
    :param collection: the Mongo collection name. Required.
    :param volume_id: the id string of the volume containing the requested HEA
    object. If None, the root volume is assumed.
    :return: a desktop object dict or None if the object was not found.
    """
    async with MongoContext(request, volume_id) as mongo:
        result = await mongo.get(request, collection, var_parts='name',
                                sub=request.headers.get(SUB))

        if result is not None:
            obj = heaobject.root.desktop_object_from_dict(result)
            permitted = has_permissions(obj=obj, sub=request.headers.get(SUB),
                                        permissions=PermissionGroup.GETTER_PERMS.perms)
            if not permitted:
                return None

        return result


async def get_all(request: Request,
                  collection: str,
                  volume_id: Optional[str] = None,
                  mongoattributes: Any | None = None,
                  sort: dict[str, Literal[-1, 1]] | None = None) -> Response:
    """
    Gets an HTTP response with all requested desktop objects in the body.
    The desktop objects are formatted according to the requested mime types in
    the HTTP request's Accept header as one of the formats supported by the
    heaserver.service.representor module.

    :param request: the HTTP request. Required.
    :param collection: the Mongo collection name. Required.
    :param volume_id: the id string of the volume containing the requested HEA
    object. If None, the root volume is assumed.
    :param sort: the sort order of the desktop objects as a dict of desktop
    object attribute to 1 or -1 for ascending or descending.
    :return: a Response with a list of HEA object dicts. If no desktop objects
    are found, the body will contain an empty list.
    """
    l = []
    async for d in get_all_gen(request, collection, volume_id, mongoattributes, sort):
        l.append(desktop_object_from_dict(d).to_dict())
    return await response.get_all(request, l)

async def get_all_dict(request: Request,
                       collection: str,
                       volume_id: str | None = None,
                       mongoattributes: Any | None = None,
                       sort: dict[str, Literal[-1, 1]] | None = None) -> list[DesktopObjectDict]:
    """
    Gets all HEA objects as a list of desktop object dicts.

    :param request: the HTTP request. Required.
    :param collection: the Mongo collection name. Required.
    :param volume_id: the id string of the volume containing the requested HEA
    object. If None, the root volume is assumed.
    :param sort: the sort order of the desktop objects as a dict of desktop
    object attribute to 1 or -1 for ascending or descending.
    :return: a list of DesktopObjectDict. If no desktop objects are found, the
    return value will be an empty list.
    """
    l = []
    async for desktop_object in get_all_gen(request, collection,
                                            volume_id=volume_id,
                                            mongoattributes=mongoattributes,
                                            sort=sort):
        l.append(desktop_object)
    return l

async def get_all_gen(request: Request,
                      collection: str,
                      volume_id: str | None = None,
                      mongoattributes: Any | None = None,
                      sort: dict[str, Literal[-1, 1]] | None = None) -> AsyncGenerator[DesktopObjectDict, None]:
    """
    Gets an async generator of all HEA objects as desktop object dicts.

    :param request: the HTTP request. Required.
    :param collection: the Mongo collection name. Required.
    :param volume_id: the id string of the volume containing the requested HEA
    object. If None, the root volume is assumed.
    :param sort: the sort order of the desktop objects as a dict of desktop
    object attribute to 1 or -1 for ascending or descending.
    :return: an async generator of DesktopObjectDicts.
    """
    sub = request.headers.get(SUB)
    async with MongoContext(request, volume_id) as mongo:
        async for r in mongo.get_all(request, collection, mongoattributes=mongoattributes, sub=sub, sort=sort):
            obj = heaobject.root.desktop_object_from_dict(r)
            if has_permissions(obj=obj,
                            sub=sub,
                            permissions=PermissionGroup.GETTER_PERMS.perms):
                yield r


async def opener(request: Request, collection: str, volume_id: str | None = None,
                 include_desktop_object: bool = True) -> Response:
    """
    Gets choices for opening an HEA desktop object's content.

    :param request: the HTTP request. Required. If an Accepts header is provided, MIME types that do not support links
    will be ignored.
    :param collection: the Mongo collection name. Required.
    :param volume_id: the id string of the volume containing the requested HEA object. If None, the root volume is
    assumed.
    :return: a Response object with status code 300, and a body containing the HEA desktop object and links
    representing possible choices for opening the HEA desktop object; or Not Found.
    """
    async with MongoContext(request, volume_id) as mongo:
        result = await mongo.get(request, collection, var_parts='id', sub=request.headers.get(SUB))
        if include_desktop_object is None:
            include_desktop_object_ = True
        else:
            include_desktop_object_ = bool(include_desktop_object)

        if result is not None:
            obj = heaobject.root.desktop_object_from_dict(result)
            permitted = has_permissions(obj=obj, sub=request.headers.get(SUB, NONE_USER), permissions=PermissionGroup.GETTER_PERMS.perms)
            if not permitted:
                return response.status_not_found()
        else:
            return response.status_not_found()

        return await response.get_multiple_choices(request, result if include_desktop_object_ else None)


async def post(request: Request, collection: str, type_: Type[DesktopObject], default_content: Optional[IO] = None, volume_id: Optional[str] = None) -> Response:
    """
    Posts the provided HEA object.

    :param request: the HTTP request.
    :param collection: the Mongo collection name. Required.
    :param type_: The HEA object type. Required.
    :param default_content: an optional blank document or other default content as a file-like object. This must be not-None
    for any microservices that manage content.
    :param volume_id: the id string of the volume containing the requested HEA object. If None, the root volume is
    assumed.
    :return: a Response object with a status of Created and the object's URI in the
    """
    try:
        obj = await new_heaobject_from_type(request, type_)
    except DeserializeException as e:
        return response.status_bad_request(str(e).encode())
    if obj.owner is None:
        obj.owner = request.headers.get(SUB, None)
    async with MongoContext(request, volume_id) as mongo:
        result = await mongo.post(request, obj, collection, default_content)
        return await response.post(request, result, collection)

async def post_dict_return_id(request: Request, obj_dict: DesktopObjectDict, collection: str, type_: Type[DesktopObject], default_content: Optional[IO] = None, volume_id: Optional[str] = None) -> str | None:
    try:
        obj = type_()
        obj.from_dict(obj_dict)
    except DeserializeException as e:
        return response.status_bad_request(str(e).encode())
    if obj.owner is None:
        obj.owner = request.headers.get(SUB, None)
    async with MongoContext(request, volume_id) as mongo:
        return await mongo.post(request, obj, collection, default_content)

async def post_dict(request: Request, obj_dict: DesktopObjectDict, collection: str, type_: Type[DesktopObject], default_content: Optional[IO] = None, volume_id: Optional[str] = None) -> Response:
    result = post_dict_return_id(request, obj_dict, collection, type_, default_content, volume_id)
    return await response.post(request, result, collection)

async def put(request: Request, collection: str, type_: Type[DesktopObject], volume_id: Optional[str] = None) -> Response:
    """
    Updates the HEA object with the specified id.

    :param request: the HTTP request. Required.
    :param collection: the Mongo collection name. Required.
    :param type_: The HEA object type. Required.
    :param volume_id: the id string of the volume containing the requested HEA object. If None, the root volume is
    assumed.
    :return: a Response object with a status of No Content, Forbidden, or Not Found.
    """
    sub = request.headers.get(SUB, None)
    async with MongoContext(request, volume_id) as mongo:
        try:
            obj = await new_heaobject_from_type(request, type_)
        except DeserializeException as e:
            return response.status_bad_request(str(e).encode())
        try:
            permitted = has_permissions(obj=obj, sub=request.headers.get(SUB), permissions=PermissionGroup.PUTTER_PERMS.perms)
            if not permitted:
                if has_permissions(obj=obj, sub=request.headers.get(SUB), permissions=PermissionGroup.GETTER_PERMS.perms):
                    return response.status_forbidden()
                else:
                    return response.status_not_found()

            result = await mongo.put(request, obj, collection, sub=sub)  # if lacks permissions or object is not in database, then updates no records.
        except WriteError as e:
            if e.code == 66:
                return response.status_bad_request(e.details['errmsg'])
            else:
                return response.status_internal_error(e.details.get('errmsg'))
        return await response.put(result.matched_count if result else False)

async def upsert(request: Request, collection: str, type_: type[DesktopObject], volume_id: str | None = None, filter: dict[str, Any] = None) -> Response:
    """
    Updates the HEA object, using the specified filter if provided otherwise the object's id, and inserting a new object
    if none matches the filter or the id.

    :param request: the HTTP request. Required.
    :param collection: the Mongo collection name. Required.
    :param type_: The HEA object type. Required.
    :param volume_id: the id string of the volume containing the requested HEA object. If None, the root volume is
    assumed.
    :param filter: optional filter criteria.
    :return: a Response object with a status of No Content, Forbidden, or Not Found.
    """
    sub = request.headers.get(SUB, None)
    async with MongoContext(request, volume_id) as mongo:
        try:
            obj = await new_heaobject_from_type(request, type_)
        except DeserializeException as e:
            return response.status_bad_request(str(e).encode())
        try:
            permitted = has_permissions(obj=obj, sub=request.headers.get(SUB), permissions=PermissionGroup.PUTTER_PERMS.perms) and \
                has_permissions(obj=obj, sub=request.headers.get(SUB), permissions=PermissionGroup.POSTER_PERMS.perms)
            if not permitted:
                if has_permissions(obj=obj, sub=request.headers.get(SUB), permissions=PermissionGroup.GETTER_PERMS.perms):
                    return response.status_forbidden()
                else:
                    return response.status_not_found()

            result = await mongo.upsert(request, obj, collection, sub=sub, mongoattributes=filter)
        except WriteError as e:
            if e.code == 66:
                return response.status_bad_request(e.details['errmsg'])
            else:
                return response.status_internal_error(e.details.get('errmsg'))
        return await response.put(result.matched_count if result else False)


async def put_content(request: Request, collection: str, type_: Type[DesktopObject], volume_id: Optional[str] = None) -> Response:
    """
    Updates the HEA object's associated content.

    :param request: the HTTP request. Required.
    :param collection: the Mongo collection name. Required.
    :param type_: The HEA object type. Required.
    :param volume_id: the id string of the volume containing the requested HEA object. If None, the root volume is
    assumed.
    :return: a Response object with a status of No Content, Forbidden, or Not Found.
    """
    async with MongoContext(request, volume_id) as mongo:
        sub = request.headers.get(SUB)
        result = await mongo.get(request, collection, var_parts='id', sub=sub)

        if result is not None:
            obj = heaobject.root.desktop_object_from_dict(result)
            permitted = has_permissions(obj=obj, sub=request.headers.get(SUB), permissions=PermissionGroup.PUTTER_PERMS.perms)
            if not permitted:
                if has_permissions(obj=obj, sub=request.headers.get(SUB), permissions=PermissionGroup.GETTER_PERMS.perms):
                    return response.status_forbidden()
                else:
                    return response.status_not_found()
            result2 = await mongo.put_content(request, collection, sub=sub)  # if lacks permissions, then updates no records.
            return await response.put(result2)
        else:
            return response.status_not_found()


async def delete(request: Request, collection: str, volume_id: Optional[str] = None) -> Response:
    """
    Deletes the HEA object with the specified id and any associated content.

    :param request: the HTTP request. Required.
    :param collection: the Mongo collection name. Required.
    :param volume_id: the id string of the volume containing the requested HEA object. If None, the root volume is
    assumed.
    :return: No Content, Forbidden, or Not Found.
    """
    async with MongoContext(request, volume_id) as mongo:
        sub = request.headers.get(SUB)
        result = await mongo.get(request, collection, var_parts='id', sub=request.headers.get(SUB))

        if result is not None:
            obj = heaobject.root.desktop_object_from_dict(result)
            permitted = has_permissions(obj=obj, sub=request.headers.get(SUB), permissions=PermissionGroup.DELETER_PERMS.perms)
            if not permitted:
                return response.status_forbidden()
            result = await mongo.delete(request, collection, var_parts='id', sub=sub)  # if lacks permissions, then deletes no records.
        else:
            return response.status_not_found()
        return await response.delete(result.deleted_count if result else False)

