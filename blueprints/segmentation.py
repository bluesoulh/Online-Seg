#分割相关
import os.path

from flask import Blueprint, request, render_template, g, redirect, url_for
from .forms import ShareForm,CommentForm
from models import ShareModel,CommentModel
from exts import db
from decorator import login_required
from semantic_segmentation import perform_semantic_segmentation

bp = Blueprint("segmentation",__name__,url_prefix="/")

@bp.route("/")
def index():
    shares = ShareModel.query.order_by(ShareModel.create_time.desc()).all()
    return render_template("index.html",shares=shares)


@bp.route("/segmentation/public", methods=['GET', 'POST'])
@login_required
def public_share():
    if request.method == 'GET':
        return render_template("public_share.html")
    else:
        form = ShareForm(request.form)
        if form.validate():
            title = form.title.data
            file = request.files.get("image")
            filename = file.filename
            filesavename = os.path.join(os.getcwd(),'static/uploaded_images', file.filename)
            file.save(filesavename)
            img_path = filename
            content = form.content.data
            share = ShareModel(title=title,image_path=img_path,content=content,author=g.user)
            db.session.add(share)
            db.session.commit()
            return redirect("/")
        else:
            print(form.errors)
            return redirect(url_for("segmentation.public_share"))

@bp.route("/segmentation/detail/<share_id>")
def share_detail(share_id):
    share = ShareModel.query.get(share_id)
    return render_template("detail.html",share=share)

@bp.post("/comment/public")
@login_required
def public_comment():
    form = CommentForm(request.form)
    if form.validate():
        content = form.content.data
        share_id = form.share_id.data
        comment = CommentModel(content=content, share_id=share_id, author_id=g.user.id)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for("segmentation.share_detail", share_id=share_id))
    else:
        print(form.errors)
        return redirect(url_for("segmentation.share_detail", share_id=request.form.get("share_id")))


@bp.route("/search")
def search():
    s = request.args.get("s")
    shares = ShareModel.query.filter(ShareModel.title.contains(s)).all()
    return render_template("index.html", shares=shares)


@bp.route("/segmentation/segm", methods=['GET', 'POST'])
@login_required
def segm():
    if request.method == 'GET':
        return render_template("segm.html")
    if request.method == 'POST':
        file = request.files.get("uploading")
        filename = os.path.join(os.getcwd(), 'static/segm_original_images', file.filename)
        file.save(filename)
        perform_semantic_segmentation(filename,file.filename)
        return redirect(url_for('segmentation.result', filename=file.filename))


@bp.route('/segmentation/result/<filename>')
def result(filename):
    return render_template('result.html',filename=filename)
