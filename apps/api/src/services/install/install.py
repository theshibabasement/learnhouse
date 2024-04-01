from datetime import datetime
from uuid import uuid4
from fastapi import HTTPException, Request
from sqlalchemy import desc
from sqlmodel import Session, select
from src.db.install import Install, InstallRead
from src.db.organizations import Organization, OrganizationCreate
from src.db.roles import Permission, Rights, Role, RoleTypeEnum
from src.db.user_organizations import UserOrganization
from src.db.users import User, UserCreate, UserRead
from config.config import get_learnhouse_config
from src.security.security import security_hash_password


async def isInstallModeEnabled():
    config = get_learnhouse_config()

    if config.general_config.install_mode:
        return True
    else:
        raise HTTPException(
            status_code=403,
            detail="Install mode is not enabled",
        )


async def create_install_instance(request: Request, data: dict, db_session: Session):
    install = Install.model_validate(data)

    # complete install instance
    install.install_uuid = str(f"install_{uuid4()}")
    install.update_date = str(datetime.now())
    install.creation_date = str(datetime.now())
    install.step = 1
    # insert install instance
    db_session.add(install)

    # commit changes
    db_session.commit()

    # refresh install instance
    db_session.refresh(install)

    install = InstallRead.model_validate(install)

    return install


async def get_latest_install_instance(request: Request, db_session: Session):
    statement = select(Install).order_by(desc(Install.creation_date)).limit(1)
    install = db_session.exec(statement).first()

    if install is None:
        raise HTTPException(
            status_code=404,
            detail="No install instance found",
        )
    
    install = InstallRead.model_validate(install)

    return install


async def update_install_instance(
    request: Request, data: dict, step: int, db_session: Session
):
    statement = select(Install).order_by(desc(Install.creation_date)).limit(1)
    install = db_session.exec(statement).first()

    if install is None:
        raise HTTPException(
            status_code=404,
            detail="No install instance found",
        )

    install.step = step
    install.data = data

    # commit changes
    db_session.commit()

    # refresh install instance
    db_session.refresh(install)

    install = InstallRead.model_validate(install)

    return install


############################################################################################################
# Steps
############################################################################################################


# Install Default roles
async def install_default_elements(db_session: Session):
    """
    """
    # remove all default roles
    statement = select(Role).where(Role.role_type == RoleTypeEnum.TYPE_GLOBAL)
    roles = db_session.exec(statement).all()

    for role in roles:
        db_session.delete(role)

    db_session.commit()

    # Check if default roles already exist
    statement = select(Role).where(Role.role_type == RoleTypeEnum.TYPE_GLOBAL)
    roles = db_session.exec(statement).all()

    if roles and len(roles) == 3:
        raise HTTPException(
            status_code=409,
            detail="Default roles already exist",
        )

    # Create default roles
    role_global_admin = Role(
        name="Admin",
        description="Standard Admin Role",
        id=1,
        role_type=RoleTypeEnum.TYPE_GLOBAL,
        role_uuid="role_global_admin",
        rights=Rights(
            courses=Permission(
                action_create=True,
                action_read=True,
                action_update=True,
                action_delete=True,
            ),
            users=Permission(
                action_create=True,
                action_read=True,
                action_update=True,
                action_delete=True,
            ),
            usergroups=Permission(
                action_create=True,
                action_read=True,
                action_update=True,
                action_delete=True,
            ),
            collections=Permission(
                action_create=True,
                action_read=True,
                action_update=True,
                action_delete=True,
            ),
            organizations=Permission(
                action_create=True,
                action_read=True,
                action_update=True,
                action_delete=True,
            ),
            coursechapters=Permission(
                action_create=True,
                action_read=True,
                action_update=True,
                action_delete=True,
            ),
            activities=Permission(
                action_create=True,
                action_read=True,
                action_update=True,
                action_delete=True,
            ),
        ),
        creation_date=str(datetime.now()),
        update_date=str(datetime.now()),
    )

    role_global_maintainer = Role(
        name="Maintainer",
        description="Standard Maintainer Role",
        id=2,
        role_type=RoleTypeEnum.TYPE_GLOBAL,
        role_uuid="role_global_maintainer",
        rights=Rights(
            courses=Permission(
                action_create=True,
                action_read=True,
                action_update=True,
                action_delete=True,
            ),
            users=Permission(
                action_create=True,
                action_read=True,
                action_update=True,
                action_delete=True,
            ),
            usergroups=Permission(
                action_create=True,
                action_read=True,
                action_update=True,
                action_delete=True,
            ),
            collections=Permission(
                action_create=True,
                action_read=True,
                action_update=True,
                action_delete=True,
            ),
            organizations=Permission(
                action_create=True,
                action_read=True,
                action_update=True,
                action_delete=True,
            ),
            coursechapters=Permission(
                action_create=True,
                action_read=True,
                action_update=True,
                action_delete=True,
            ),
            activities=Permission(
                action_create=True,
                action_read=True,
                action_update=True,
                action_delete=True,
            ),
        ),
        creation_date=str(datetime.now()),
        update_date=str(datetime.now()),
    )

    role_global_user = Role(
        name="User",
        description="Standard User Role",
        role_type=RoleTypeEnum.TYPE_GLOBAL,
        role_uuid="role_global_user",
        id=3,
        rights=Rights(
            courses=Permission(
                action_create=False,
                action_read=True,
                action_update=False,
                action_delete=False,
            ),
            users=Permission(
                action_create=True,
                action_read=True,
                action_update=False,
                action_delete=False,
            ),
            usergroups=Permission(
                action_create=False,
                action_read=True,
                action_update=False,
                action_delete=False,
            ),
            collections=Permission(
                action_create=False,
                action_read=True,
                action_update=False,
                action_delete=False,
            ),
            organizations=Permission(
                action_create=False,
                action_read=True,
                action_update=False,
                action_delete=False,
            ),
            coursechapters=Permission(
                action_create=False,
                action_read=True,
                action_update=False,
                action_delete=False,
            ),
            activities=Permission(
                action_create=False,
                action_read=True,
                action_update=False,
                action_delete=False,
            ),
        ),
        creation_date=str(datetime.now()),
        update_date=str(datetime.now()),
    )

    # Serialize rights to JSON
    role_global_admin.rights = role_global_admin.rights.model_dump()  # type: ignore
    role_global_maintainer.rights = role_global_maintainer.rights.model_dump()  # type: ignore
    role_global_user.rights = role_global_user.rights.model_dump()  # type: ignore

    # Insert roles in DB
    db_session.add(role_global_admin)
    db_session.add(role_global_maintainer)
    db_session.add(role_global_user)

    # commit changes
    db_session.commit()

    # refresh roles
    db_session.refresh(role_global_admin)

    return True


# Organization creation
async def install_create_organization(
     org_object: OrganizationCreate, db_session: Session
):
    org = Organization.model_validate(org_object)

    # Complete the org object
    org.org_uuid = f"org_{uuid4()}"
    org.creation_date = str(datetime.now())
    org.update_date = str(datetime.now())

    db_session.add(org)
    db_session.commit()
    db_session.refresh(org)

    return org


async def install_create_organization_user(
     user_object: UserCreate, org_slug: str, db_session: Session
):
    user = User.model_validate(user_object)

    # Complete the user object
    user.user_uuid = f"user_{uuid4()}"
    user.password = await security_hash_password(user_object.password)
    user.email_verified = False
    user.creation_date = str(datetime.now())
    user.update_date = str(datetime.now())

    # Verifications

    # Check if Organization exists
    statement = select(Organization).where(Organization.slug == org_slug)
    org = db_session.exec(statement)

    if not org.first():
        raise HTTPException(
            status_code=409,
            detail="Organization does not exist",
        )

    # Username
    statement = select(User).where(User.username == user.username)
    result = db_session.exec(statement)

    if result.first():
        raise HTTPException(
            status_code=409,
            detail="Username already exists",
        )

    # Email
    statement = select(User).where(User.email == user.email)
    result = db_session.exec(statement)

    if result.first():
        raise HTTPException(
            status_code=409,
            detail="Email already exists",
        )

    # Exclude unset values
    user_data = user.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(user, key, value)

    # Add user to database
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    

    # get org id
    statement = select(Organization).where(Organization.slug == org_slug)
    org = db_session.exec(statement)
    org = org.first()
    org_id = org.id if org else 0

    # Link user and organization
    user_organization = UserOrganization(
        user_id=user.id if user.id else 0,
        org_id=org_id or 0,
        role_id=1,
        creation_date=str(datetime.now()),
        update_date=str(datetime.now()),
    )

    db_session.add(user_organization)
    db_session.commit()
    db_session.refresh(user_organization)

    user = UserRead.model_validate(user)

    return user
