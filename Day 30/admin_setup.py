from database import SessionLocal

from models.user import User


# ============================================================
# CREATE / PROMOTE ADMIN
# ============================================================

db = SessionLocal()


email = input(
    "Enter user email to make admin: "
).strip()


user = (
    db.query(User)
    .filter(
        User.email == email
    )
    .first()
)


if not user:

    print(
        "User not found. "
        "Register the user first."
    )

else:

    user.role = "admin"

    db.commit()

    print(
        f"{user.email} is now an ADMIN."
    )


db.close()