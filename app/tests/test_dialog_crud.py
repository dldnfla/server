import datetime

from .. import crud, schemas


def test_create_dialog(session):
    dialog_create = schemas.DialogCreate(
        user_id=1,
        visitor="tester",
        contents="testing",
    )

    dialog = crud.create_dialog(session, dialog_create)

    for k in ["user_id", "visitor", "contents"]:
        assert getattr(dialog, k) == getattr(dialog_create, k)


def test_get_dialog(session, test_dialogs):
    response = crud.get_dialog(
        session, user_id=test_dialogs[0].user_id, skip=0, limit=2
    )

    for val, exp in zip(response, test_dialogs):
        for k in ["user_id", "visitor", "contents"]:
            print(getattr(exp, k))
            assert getattr(val, k) == getattr(exp, k), k


def test_update_todo(session, test_todo):
    crud.update_todo(
        session, todo=schemas.TodoEdit(**test_todo), todo_id=test_todo["id"]
    )

    new_todo = crud.get_todo(session, test_todo["id"])

    for k in ["user_id", "icon", "title", "contents", "color", "done"]:
        assert getattr(new_todo, k) == test_todo[k]


def test_delete_todo(session, test_todo):
    crud.delete_todo(session, test_todo["id"])

    todo = crud.get_todo(session, test_todo["id"])

    assert todo is None
