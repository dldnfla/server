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

    # 반복문 걸어서 assert로 확인 print는 그냥 내가 오류 생겨서 값 직접 찍어본거 없어도 무방
    for val, exp in zip(response, test_dialogs):
        for k in ["user_id", "visitor", "contents"]:
            # print(getattr(exp, k))
            assert getattr(val, k) == getattr(exp, k), k


def test_update_dialog(session, test_dialog):
    crud.update_dialog(
        session,
        new_dialog=schemas.DialogEdit(**test_dialog),
        dialog_id=test_dialog["id"],
    )
    print("ndjasnfjanvnka")
    new_dialog = crud.get_dialog(session, user_id=test_dialog["user_id"])

    for k in ["user_id", "visitor", "contents"]:
        assert getattr(new_dialog[0], k) == test_dialog[k]
