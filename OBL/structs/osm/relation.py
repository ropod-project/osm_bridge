from OBL.structs.osm.tag import Tag

class Member(object):
    '''
    OSM relation member
    '''
    def __init__(self, elm):
        element = elm
        self.ref = element.get('ref')
        self.role = element.get('role')
        self.type = element.get('type')

    def __repr__(self):
        return "<Member ref=%(ref)s role=%(role)s> type=%(type)s" % { 'ref': self.ref, 'role': self.role, 'type': self.type }

class Relation(object):
    '''
    OSM relation
    '''
    def __init__(self, elm):
        element = elm
        self.id = element.get('id')

        self.tags = []
        tags = element.get('tags')
        if tags is not None:
            for tag in tags:
                self.tags.append(Tag(tag, tags.get(tag))) 

        members = element.get('members')
        self.members = []
        for member in members:
            self.members.append(Member(member)) 

    def __eq__(self, other):
        return other is not None and self.id == other.id

    def __repr__(self):
        return "<Relation id=%(id)s type=%(type)s>" % { 'id': self.id, 'type': self.type }

    def __getattr__(self, item):
        return None
