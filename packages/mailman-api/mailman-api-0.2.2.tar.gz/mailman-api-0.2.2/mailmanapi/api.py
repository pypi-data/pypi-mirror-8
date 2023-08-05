
import os
import uuid

from bottle import route, request, template, default_app
from Mailman import Utils, Errors, Post, mm_cfg

from .members import Member
from .utils import parse_boolean, jsonify, get_mailinglist, get_timestamp


CWD = os.path.abspath(os.path.dirname(__file__))
EMAIL_TEMPLATE = os.path.join(CWD, 'templates', 'message.tpl')


@route('/', method='GET')
def list_lists():
    all_lists = Utils.list_names()
    lists = []

    include_description = request.query.get('description')

    address = request.query.get('address')
    for listname in all_lists:
        mlist = get_mailinglist(listname, lock=False)
        members = mlist.getMembers()
        if not address or address in members:
            if include_description:
                lists.append((listname, mlist.description.decode('latin1')))
            else:
                lists.append(listname)

    return jsonify(lists)


@route('/<listname>', method='PUT')
def subscribe(listname):
    address = request.forms.get('address')
    fullname = request.forms.get('fullname')
    digest = parse_boolean(request.forms.get('digest'))

    mlist = get_mailinglist(listname)
    userdesc = Member(fullname, address, digest)

    try:
        mlist.ApprovedAddMember(userdesc, ack=True, admin_notif=True)
    except Errors.MMAlreadyAMember:
        return jsonify("Address already a member.", 409)
    except Errors.MembershipIsBanned:
        return jsonify("Banned address.", 403)
    except (Errors.MMBadEmailError, Errors.MMHostileAddress):
        return jsonify("Invalid address.", 400)

    else:
        mlist.Save()
    finally:
        mlist.Unlock()

    return jsonify(True)


@route('/<listname>', method='DELETE')
def unsubscribe(listname):
    address = request.forms.get('address')
    mlist = get_mailinglist(listname)

    try:
        mlist.ApprovedDeleteMember(address, admin_notif=False, userack=True)
        mlist.Save()
    except Errors.NotAMemberError:
        return jsonify("Not a member.", 404)
    finally:
        mlist.Unlock()

    return jsonify(True)


@route('/<listname>', method='GET')
def members(listname):
    mlist = get_mailinglist(listname, lock=False)
    return jsonify(mlist.getMembers())


@route('/<listname>/sendmail', method='POST')
def sendmail(listname):
    mlist = get_mailinglist(listname, lock=False)

    context = {}
    context['email_to'] = mlist.GetListEmail()
    context['message_id'] = uuid.uuid1()
    context['ip_from'] = request.environ.get('REMOTE_ADDR')
    context['timestamp'] = get_timestamp()

    context['name_from'] = request.forms.get('name_from')
    context['email_from'] = request.forms.get('email_from')
    context['subject'] = request.forms.get('subject')
    context['body'] = request.forms.get('body')

    in_reply_to = request.forms.get('in_reply_to')
    if in_reply_to:
        context['in_reply_to'] = in_reply_to

    if None in context.values():
        return jsonify('Missing information. `email_from`, `subject` and '
                       '`body` are mandatory', 400)

    email = template(EMAIL_TEMPLATE, context)
    Post.inject(listname, email.encode('utf8'), qdir=mm_cfg.INQUEUE_DIR)
    return jsonify(True)


def get_application(allowed_ips):
    bottle_app = default_app()
    def application(environ, start_response):
        if environ['REMOTE_ADDR'] not in allowed_ips:
            status = '403 FORBIDDEN'
            headers = [('Content-type', 'text/plain')]
            start_response(status, headers)
            return 'FORBIDDEN'

        return bottle_app(environ, start_response)
    return application
