from flask import Flask
from flask_restful import Api ,Resource,reqparse,abort,fields,marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///database.db'
db=SQLAlchemy(app)

class ImgModel(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    desc = db.Column(db.String(100),nullable=False)
    likes = db.Column(db.Integer,nullable=False)
    comments = db.Column(db.Integer,nullable=False)

    def __repr__(self):
        return f"IMG (desc={self.desc},likes={self.likes},comments={self.comments})"

img_put_args = reqparse.RequestParser()
img_put_args.add_argument("desc",type=str,help="description about image")
img_put_args.add_argument("likes",type=int,help="no of likes")
img_put_args.add_argument("comments",type=int,help="no of comments")


resource_fields={
    'id':fields.Integer,
    'desc':fields.String,
    'likes':fields.Integer,
    'comments':fields.Integer
}

class img(Resource):
    @marshal_with(resource_fields)
    def get(self,img_id):
        result=ImgModel.query.filter_by(id=img_id).first()
        if not result:
            abort(404,message="id not found")
        return result
    
    @marshal_with(resource_fields)
    def put(self,img_id):
        args = img_put_args.parse_args()
        i=ImgModel.query.filter_by(id=img_id).first()
        if i:
            abort(409,message="id has taken")
        result=ImgModel(id=img_id,desc=args['desc'],likes=args['likes'],comments=args['comments'])
        db.session.add(result)
        db.session.commit()
        return result,201
    
    @marshal_with(resource_fields)
    def patch(self,img_id):
        args = img_put_args.parse_args()
        result=ImgModel.query.filter_by(id=img_id).first()
        if not result:
            abort(404,message="id not found")
        if args['desc']:
            result.desc=args['desc']
        if args['likes']:
            result.likes=args['likes']
        if args['comments']:
            result.comments=args['comments']
        
        db.session.commit()
        return result

    @marshal_with(resource_fields)
    def delete(self,img_id):
        result=ImgModel.query.filter_by(id=img_id).first()
        if not result:
            abort(404,message="id not found")
        db.session.delete(result)
        db.session.commit()
        return result

api.add_resource(img,"/img/<int:img_id>")

if __name__ == "__main__":
    app.run(debug=True)