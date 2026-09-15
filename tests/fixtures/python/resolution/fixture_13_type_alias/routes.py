from deps import RepoDep, SessionDep


def create_order(repo: RepoDep, session: SessionDep, order):
    session.commit()
    return repo.save(order)
