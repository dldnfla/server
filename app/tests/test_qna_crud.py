import datetime

from .. import crud, schemas


def test_get_qna(session, test_qna_answer):
    response = crud.get_qna(
        session, user_id=test_qna_answer.user_id, skip=0, limit=2
    )

    for val, exp in zip(response, test_qna_answer):
        for k in ["user_id", "answer1", "answer2", "answer3", "answer4", "answer5", "answer6", "answer7", "answer8", "answer9", "answer10"]:
            assert getattr(val, k) == getattr(exp, k), k


def test_update_qna(session, test_qna):
    crud.update_qna(
        session,
        new_qna=schemas.QnaEdit(**test_qna),
        user_id=test_qna["user_id"],
    )
    
    new_qna = crud.get_qna(session, user_id=test_qna["user_id"])

    # 필드 값 검증
    for k in ["user_id", "answer1", "answer2", "answer3", "answer4", "answer5", "answer6", "answer7", "answer8", "answer9", "answer10"]:
        assert getattr(new_qna[0], k) == test_qna[k]
