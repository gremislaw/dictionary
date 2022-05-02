from flask import request, Blueprint, render_template, flash
from . import db_session
from .word import Word, search_word, add_new_word


blueprint = Blueprint(
    'words_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/words/<string:word_name>', methods=['POST', 'GET'])
def get_word(word_name):
    db_sess = db_session.create_session()
    words = db_sess.query(Word).filter(Word.name == word_name).all()
    if request.method == 'GET':
        if word_name == '0':
            return render_template('word_menu.html', title="Не нейдено", objects=[])

        return render_template('word_menu.html', title="Значение слова " + words[0].name.upper(),
                                     objects=words)
    elif request.method == 'POST':
        if request.form['some_button'] == 'add_word':
            name_new = request.form['new_word_name'].capitalize()
            about_new = request.form['new_word_about'].lower()
            translate_new = request.form['new_word_translate'].lower()
            add_new_word(name_new, about_new, translate_new)
            flash("Слово успешно добавлено", 'success')
            return render_template('word_menu.html', title="Значение слова " + words[0].name.upper(),
                                   objects=words)
        name = request.form['search'].capitalize()
        return search_word(name)
