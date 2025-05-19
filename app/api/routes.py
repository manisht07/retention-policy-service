
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.schemas import *
from app.models import RetentionPolicy
from app.database import get_db
from app.services.rule_engine import evaluate_policy

router = APIRouter()

@router.post("/", response_model=RetentionPolicyOut)
def create_policy(payload: RetentionPolicyCreate, db: Session = Depends(get_db)):
    policy = RetentionPolicy(**payload.dict())
    db.add(policy)
    db.commit()
    db.refresh(policy)
    return policy

@router.get("/", response_model=List[RetentionPolicyOut])
def list_policies(db: Session = Depends(get_db)):
    return db.query(RetentionPolicy).all()

@router.get("/{policy_id}", response_model=RetentionPolicyOut)
def get_policy(policy_id: UUID, db: Session = Depends(get_db)):
    policy = db.query(RetentionPolicy).get(policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    return policy

@router.put("/{policy_id}", response_model=RetentionPolicyOut)
def update_policy(policy_id: UUID, payload: RetentionPolicyUpdate, db: Session = Depends(get_db)):
    policy = db.query(RetentionPolicy).get(policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    for key, value in payload.dict(exclude_unset=True).items():
        setattr(policy, key, value)
    db.commit()
    db.refresh(policy)
    return policy

@router.delete("/{policy_id}")
def delete_policy(policy_id: UUID, db: Session = Depends(get_db)):
    policy = db.query(RetentionPolicy).get(policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    db.delete(policy)
    db.commit()
    return {"detail": "Policy deleted successfully"}


@router.post("/evaluate/{policy_id}")
def evaluate_record(policy_id: UUID, record: dict, db: Session = Depends(get_db)):
    policy = db.query(RetentionPolicy).get(policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    return {
        "expiration_date": evaluate_policy(policy.__dict__, record)
    }

