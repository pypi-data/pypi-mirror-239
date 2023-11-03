from datetime import datetime, timedelta
from typing import Any

import pytz
from google.cloud import firestore
from hubspot.crm.schemas import ObjectSchema

from ..core.utils import timed_lru_cache
from .base import BaseService
from ..models.hubspot.workflow_actions import WorkflowOptionsResponse
from ..models.oauth.tokens import Token


class FirestoreService(BaseService):
    def __init__(
        self,
        firestore_client: firestore.Client
    ) -> None:
        self.firestore_client = firestore_client
        super().__init__(
            log_name='firestore.service',
            exclude_inputs=[
                'set_account_connection'
            ],
            exclude_outputs=[
                'get_account_connection'
            ]
        )

    def get_app_docs(self):
        return self.firestore_client.collection('apps').list_documents()

    def get_account_doc(self, app_name: str, account_id: [int | str]):
        app_doc = self.firestore_client.collection(
            'apps'
        ).document(
            app_name
        )
        if not app_doc.get().exists:
            app_doc.set(
                {'created': datetime.now()}
            )

        account_doc = app_doc.collection(
            'accounts'
        ).document(
            str(account_id)
        )
        if not account_doc.get().exists:
            account_doc.set(
                {'created': datetime.now()}
            )
        return account_doc

    @timed_lru_cache(seconds=180)
    def get_account_connection(self, app_name: str, account_id: [int | str]) -> Token:
        connection_doc = self.get_account_doc(
            app_name=app_name,
            account_id=account_id
        ).collection(
            'settings'
        ).document(
            'connection'
        ).get()
        return Token(**connection_doc.to_dict())

    def set_account_connection(self, app_name: str, account_id: [int | str], token: dict):
        if 'expires_in' in token:
            token['expires_at'] = int((datetime.now() + timedelta(seconds=token['expires_in'] - 60)).timestamp())
        connection_doc = self.get_account_doc(
            app_name=app_name,
            account_id=account_id
        ).collection(
            'settings'
        ).document(
            'connection'
        )
        connection_doc.update(token) if connection_doc.get().exists else connection_doc.set(document_data=token)

    def get_object_schema(self, app_name: str, account_id: Any, object_type: str):
        objects_doc = self.get_account_doc(
            app_name=app_name,
            account_id=account_id
        ).collection(
            'settings'
        ).document(
            'objects'
        )
        if not objects_doc.get().exists:
            objects_doc.set(
                {'created': datetime.now()}
            )
        doc = objects_doc.collection(
            object_type
        ).document('schema')
        object_schema = dict() if not doc.get().exists else ObjectSchema(**doc.get().to_dict())
        return object_schema

    def set_object_schema(self, app_name: str, account_id: str, object_type: str, object_schema: ObjectSchema):
        objects_doc = self.get_account_doc(
            app_name=app_name,
            account_id=account_id
        ).collection(
            'settings'
        ).document(
            'objects'
        )
        if not objects_doc.get().exists:
            objects_doc.set(
                {'created': datetime.now()}
            )
        doc = objects_doc.collection(
            object_type
        ).document('schema')
        doc_data = dict() if not doc.get().exists else doc.get().to_dict()
        doc.set(document_data=doc_data | object_schema.to_dict())

    def get_app_account_ids(self, app_name: str):
        collection = self.firestore_client.collection('apps').document(
            document_id=app_name
        ).collection('accounts')

        return [account_doc.id for account_doc in collection.stream()]

    def get_app_account_field(self, app_name: str, account_id: Any, field_name: str):
        doc = self.get_account_doc(
            app_name=app_name,
            account_id=str(account_id)
        )
        doc_data = dict() if not doc.get().exists else doc.get().to_dict()
        return doc_data.get(field_name)

    def set_app_account_field(self, app_name: str, account_id: Any, field_name: str, value: Any = None):
        doc = self.get_account_doc(
            app_name=app_name,
            account_id=account_id
        )
        doc_data = dict() if not doc.get().exists else doc.get().to_dict()
        doc_data[field_name] = value
        return doc.set(document_data=doc_data)

    def get_object_properties(
        self,
        app_name: str,
        account_id: [int | str],
        object_type: str,
        field_type: str = None,
        referenced_object_type: str = None
    ):
        field_type = field_type if field_type else ''
        referenced_object_type = referenced_object_type if referenced_object_type else ''
        properties_doc = self.get_account_doc(
            app_name=app_name,
            account_id=account_id
        ).collection(
            'object_properties'
        ).document(
            f"{object_type}-{field_type}{referenced_object_type}"
        ).get()
        return properties_doc.to_dict() if properties_doc.exists else WorkflowOptionsResponse(options=[]).model_dump()

    def set_object_properties(
        self,
        app_name: str,
        account_id: [int | str],
        object_type: str,
        object_properties: dict,
        field_type: str = '',
        referenced_object_type: str = ''
    ):
        objects_doc = self.get_account_doc(
            app_name=app_name,
            account_id=account_id
        ).collection(
            'object_properties'
        ).document(
            f"{object_type}-{field_type}{referenced_object_type}"
        )
        objects_doc.set(document_data=object_properties)

    def delete_account(self, app_name: str, account_id: Any):
        account_doc = self.get_account_doc(
            app_name=app_name,
            account_id=account_id
        )
        self.firestore_client.recursive_delete(reference=account_doc)

    def delete_doc(self, doc_ref: Any):
        self.firestore_client.recursive_delete(reference=doc_ref)

    def read_recursive(
        self,
        source: firestore.CollectionReference,
        target: firestore.CollectionReference,
        batch: firestore.WriteBatch,
    ) -> None:
        batch_nr = 0

        for source_doc_ref in source.stream():
            document_data = source_doc_ref.to_dict()
            target_doc_ref = target.document(source_doc_ref.id)
            if batch_nr == 500:
                print("Committing %s batched operations..." % batch_nr)
                batch.commit()
                batch_nr = 0
            batch.set(
                reference=target_doc_ref,
                document_data=document_data,
                merge=False,
            )
            batch_nr += 1
            for source_coll_ref in source.document(source_doc_ref.id).collections():
                target_coll_ref = target_doc_ref.collection(source_coll_ref.id)
                self.read_recursive(
                    source=source_coll_ref,
                    target=target_coll_ref,
                    batch=batch,
                )

    def copy_collection(
        self,
        source: str,
        target: str,
    ):
        batch = self.firestore_client.batch()
        self.read_recursive(
            source=self.firestore_client.collection(source),
            target=self.firestore_client.collection(target),
            batch=batch,
        )
        batch.commit()

    def object_currently_enrolled(
        self,
        portal_id: int,
        workflow_id: int,
        action_id: int,
        object_type: str,
        object_id: int,
        callback_id: str
    ):
        enrollment_key = f"{portal_id}-{workflow_id}-{action_id}-{object_type}-{object_id}"
        enrollment_doc = self.firestore_client.collection(
            'enrollments'
        ).document(
            enrollment_key
        )
        est = pytz.timezone('US/Eastern')
        utc = pytz.utc
        now = datetime.now(tz=utc).astimezone(est)
        doc = enrollment_doc.get()
        doc_obj = doc.to_dict()
        if not doc.exists or doc_obj['expires'] < now:
            enrollment_doc.set(
                {
                    'expires': now + timedelta(hours=2),
                    'callback_ids': [callback_id],
                    'completed': False
                }
            )
            return False
        enrollment_doc.set(
            {
                'expires': doc_obj['expires'],
                'callback_ids': list(set(doc_obj['callback_ids'] + [callback_id])),
                'completed': doc_obj['completed']
            }
        )

        if not doc_obj['completed']:
            return False
        return True

    def get_enrollments(
        self,
        portal_id: int,
        workflow_id: int,
        action_id: int,
        object_type: str,
        object_id: int,
        callback_id: str
    ):
        enrollment_key = f"{portal_id}-{workflow_id}-{action_id}-{object_type}-{object_id}"
        enrollment_doc = self.firestore_client.collection(
            'enrollments'
        ).document(
            enrollment_key
        )
        if not enrollment_doc.get().exists:
            return [callback_id]
        doc = enrollment_doc.get()
        doc_obj = doc.to_dict()
        callback_ids = list(set(doc_obj['callback_ids'] + [callback_id]))
        return callback_ids

    def complete_enrollment(
        self,
        portal_id: int,
        workflow_id: int,
        action_id: int,
        object_type: str,
        object_id: int
    ):
        enrollment_key = f"{portal_id}-{workflow_id}-{action_id}-{object_type}-{object_id}"
        enrollment_doc = self.firestore_client.collection(
            'enrollments'
        ).document(
            enrollment_key
        )
        doc = enrollment_doc.get()
        doc_obj = doc.to_dict()
        enrollment_doc.set(
            {
                'expires': enrollment_doc.get().to_dict()['expires'],
                'callback_ids': doc_obj['callback_ids'],
                'completed': True
            }
        )

    def clear_enrollments(
        self,
        portal_id: int,
        workflow_id: int,
        action_id: int,
        object_type: str,
        object_id: int
    ):
        enrollment_key = f"{portal_id}-{workflow_id}-{action_id}-{object_type}-{object_id}"
        enrollment_doc = self.firestore_client.collection(
            'enrollments'
        ).document(
            enrollment_key
        )
        data = enrollment_doc.get().to_dict()
        data['callback_ids'] = []
        enrollment_doc.set(data)
