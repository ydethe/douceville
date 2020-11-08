from douceville.models import *


q = User.query.delete()
db.session.commit()
