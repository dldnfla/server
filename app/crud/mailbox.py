from sqlalchemy.orm import Session

from .. import models, schemas


def create_mailbox(db: Session, mailbox: schemas.MailboxCreate):
    db_mailbox = models.Mailbox(
        title=mailbox.title,
        recipient=mailbox.recipient,
        sender=mailbox.sender,
        content=mailbox.content,
        date=mailbox.date,
    )
    db.add(db_mailbox)
    db.commit()
    db.refresh(db_mailbox)

    return db_mailbox
