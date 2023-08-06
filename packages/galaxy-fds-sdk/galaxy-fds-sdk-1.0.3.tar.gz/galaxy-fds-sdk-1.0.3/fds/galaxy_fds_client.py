#!/usr/bin/env python
import requests
import json

from fds.auth.common import Common
from fds.auth.signature.signer import Signer
from fds.model.access_control_policy import AccessControlPolicy
from fds.model.fds_object_metadata import FDSObjectMetadata
from fds.model.permission import Owner
from fds.model.permission import AccessControlList
from fds.model.permission import Grant
from fds.model.permission import Grantee
from fds.model.subresource import SubResource
from galaxy_fds_client_exception import GalaxyFDSClientException

#
#Users use GalaxyFDSClient create client objects to access the FDS services.
#@parameters:access_key,it is required,users can apply it from dev.xiaomi.com
#@parameters:access_secret,it is required,users can apply from dev.xiaomi.com
#@parameters:uri,it is not required,the default uri is http://files.fds.api.xiaomi.com/
#
class GalaxyFDSClient(object):
    def __init__(self, access_key, access_secret, uri=None):
        self._delimiter = "/"
        self._access_key = access_key
        self._access_secret = access_secret
        self._auth = Signer(self._access_key, self._access_secret)
        if uri:
            self._fds_base_uri = self._check_uri(uri)
        else:
            self._fds_base_uri = Common.DEFAULT_FDS_SERVICE_BASE_URI

    @staticmethod
    def _check_uri(uri):
        if uri.endswith("/") is False:
            return '%s/' % uri
        return uri
    #
    #Check the existence of a bucket
    #@parameters:bucket_name
    #@return:True/False
    #
    def does_bucket_exist(self, bucket_name):
        uri = '%s%s' % (self._fds_base_uri, bucket_name)
        response = requests.head(uri, auth=self._auth)
        if response.status_code == requests.codes.ok:
            return True
        elif response.status_code == requests.codes.not_found:
            return False
        else:
            message = 'Check bucket existence failed,status=%s,reason=%s' % (response.status_code, response.content)
            raise GalaxyFDSClientException(message)
    #
    #Return a list of all the user's owning buckets.
    #
    def list_buckets(self):
        uri = self._fds_base_uri
        response = requests.get(uri, auth=self._auth)
        if response.status_code != requests.codes.ok:
            message = 'List buckets failed,status=%s,reason=%s' % (response.status_code, response.content)
            raise GalaxyFDSClientException(message)
        elif response.content is not '':
            buckets_list = []
            buckets = json.loads(response.content)['buckets']
            for bucket in buckets:
                buckets_list.append(bucket['name'])
            return buckets_list
        else:
            return []

    #
    #Creat a bucket,its owner is who created it.
    #@parameters:bucket_name
    #
    def create_bucket(self, bucket_name):
        uri = '%s%s' % (self._fds_base_uri, bucket_name)
        response = requests.put(uri, auth=self._auth)
        print response.status_code
        if response.status_code != requests.codes.ok:
            message = 'Create bucket failed,status=%s,reason=%s' % (response.status_code, response.content)
            raise GalaxyFDSClientException(message)

    #
    #Delete a bucket,the user should have FULL_CONTROL permission of the bucket.
    #@parameters:bucket_name
    #
    def delete_bucket(self, bucket_name):
        uri = '%s%s' % (self._fds_base_uri, bucket_name)
        response = requests.delete(uri, auth=self._auth)
        if response.status_code != requests.codes.ok:
            message = 'Delete bucket failed,status=%s,reason=%s' % (response.status_code, response.content)
            raise GalaxyFDSClientException(message)

    #
    #Put a object into a bucket,the user should have WRITE or FULL_CONTROL permission of the bucket.
    #@parameters:bucket_name,object_name and object content are required,
    #@parameters:metadata is not required.
    #
    def put_object(self, bucket_name, object_name, content, metadata=None):
        uri = '%s%s/%s' % (self._fds_base_uri, bucket_name, object_name)
        response = requests.put(uri, data=content, auth=self._auth, headers=metadata)
        if response.status_code != requests.codes.ok:
            message = 'Put object failed,status=%s,reason=%s' % (response.status_code, response.content)
            raise GalaxyFDSClientException(message)

    #
    #When put a large object,users can split it into some parts,and use an iterator object to
    #put these parts one by one.
    #@parameters:bucket_name,object_name and iterator are required,
    #@parameters:metadata is not required.
    #
    def stream_put_object(self, bucket_name, object_name, iterator, metadata=None):
        uri = '%s%s/%s' % (self._fds_base_uri, bucket_name, object_name)
        response = requests.put(uri, data=iterator, auth=self._auth, headers=metadata)
        if response.status_code != requests.codes.ok:
            message = 'Put object failed,status=%s,reason=%s' % (response.status_code, response.content)
            raise GalaxyFDSClientException(message)
    #
    #Users can put an object without define its name.
    #@parameters:bucket_name and object content are required,
    #@parameters:metadata is not required.
    #
    def post_object(self, bucket_name, content, metadata=None):
        uri = '%s%s/' % (self._fds_base_uri, bucket_name)
        response = requests.post(uri, data=content, auth=self._auth, headers=metadata)
        if response.status_code != requests.codes.ok:
            message = 'Post object failed,status=%s,reason=%s' % (response.status_code, response.content)
            raise GalaxyFDSClientException(message)

    #
    #Get a object from a bucket,the user should have at least READ permission of the bucket or object.
    #
    def get_object(self, bucket_name, object_name):
        uri = '%s%s/%s' % (self._fds_base_uri, bucket_name, object_name)
        response = requests.get(uri, auth=self._auth)
        if response.status_code == requests.codes.ok:
            return response.content
        else:
            message = 'Get object failed,status=%s,reason=%s' % (response.status_code, response.content)
            raise GalaxyFDSClientException(message)


    def stream_get_object(self, bucket_name, object_name, size=5 * 1024 * 1024):
        if size <= 0:
            message = 'Stream get object failed, chunk size is=%s' % size
            raise GalaxyFDSClientException(message)
        uri = '%s%s/%s' % (self._fds_base_uri, bucket_name, object_name)
        response = requests.get(uri, auth=self._auth, stream=True)
        if response.status_code == requests.codes.ok:
            for chunk in response.iter_content(chunk_size=size):
                if chunk:
                    yield chunk
        else:
            message = 'Stream get object failed,status=%s,reason=%s' % (response.status_code, response.content)
            raise GalaxyFDSClientException(message)


    def does_object_exists(self, bucket_name, object_name):
        uri = '%s%s/%s' % (self._fds_base_uri, bucket_name, object_name)
        response = requests.head(uri, auth=self._auth)
        if response.status_code == requests.codes.ok:
            return True
        elif response.status_code == requests.codes.not_found:
            return False
        else:
            message = 'Check object existence failed,status=%s,reason=%s' % (response.status_code, response.content)
            raise GalaxyFDSClientException(message)

    def delete_object(self, bucket_name, object_name):
        uri = '%s%s/%s' % (self._fds_base_uri, bucket_name, object_name)
        response = requests.delete(uri, auth=self._auth)
        if response.status_code != requests.codes.ok:
            message = 'Delete object failed,status=%s,reason=%s' % (response.status_code, response.content)
            raise GalaxyFDSClientException(message)

    def get_object_size(self, bucket_name, object_name):
        uri = '%s%s/%s' % (self._fds_base_uri, bucket_name, object_name)
        response = requests.get(uri, auth=self._auth)
        if response.status_code == requests.codes.ok:
            return response.headers['content-length']
        else:
            message = 'Get object size failed,status=%s,reason=%s' % (response.status_code, response.content)
            raise GalaxyFDSClientException(message)

    def rename_object(self, bucket_name, src_object_name, dst_object_name):
        uri = '%s%s/%s?renameTo=%s' % (self._fds_base_uri, bucket_name, src_object_name, dst_object_name)
        response = requests.put(uri, auth=self._auth)
        if response.status_code != requests.codes.ok:
            message = 'Rename object failed,status=%s,reason=%s' % (response.status_code, response.content)
            raise GalaxyFDSClientException(message)

    def list_objects(self, bucket_name, prefix=''):
        uri = '%s%s?prefix=%s&delimiter=%s' % (self._fds_base_uri, bucket_name, prefix, self._delimiter)
        response = requests.get(uri, auth=self._auth)
        if response.status_code == requests.codes.ok:
            objects_list = []
            objects = json.loads(response.content)['objects']
            for k in objects:
                objects_list.append(k['name'])
            return objects_list
        else:
            message = 'List objects failed,status=%s,reason=%s' % (response.status_code, response.content)
            raise GalaxyFDSClientException(message)

    def list_directories(self, bucket_name, prefix=''):
        uri = '%s%s?prefix=%s&delimiter=%s' % (self._fds_base_uri, bucket_name, prefix, self._delimiter)
        response = requests.get(uri, auth=self._auth)
        if response.status_code == requests.codes.ok:
            directories = json.loads(response.content)['commonPrefixes']
            return directories
        else:
            message = 'List directories failed,status=%s,reason=%s' % (response.status_code, response.content)
            raise GalaxyFDSClientException(message)

    def list_directories_and_objects(self, bucket_name, prefix=''):
        uri = '%s%s?prefix=%s&delimiter=%s' % (self._fds_base_uri, bucket_name, prefix, self._delimiter)
        response = requests.get(uri, auth=self._auth)
        result_list = []
        if response.status_code == requests.codes.ok:
            directories = json.loads(response.content)['commonPrefixes']
            objects_list = []
            objects = json.loads(response.content)['objects']
            for k in objects:
                objects_list.append(k['name'])
            result_list.extend(directories + objects_list)
            return result_list
        else:
            message = 'List directories and objects failed,status=%s,reason=%s' % (
            response.status_code, response.content)
            raise GalaxyFDSClientException(message)

    def set_bucket_acl(self, bucket_name, acl=None):
        uri = '%s%s?%s' % (self._fds_base_uri, bucket_name, SubResource.ACL)
        acp = self.__acl_to_acp(acl)
        response = requests.put(uri, auth=self._auth, data=json.dumps(acp))
        if response.status_code != requests.codes.ok:
            message = 'Set bucket acl failed,status=%s,reason=%s' % (response.status_code, response.content)
            raise GalaxyFDSClientException(message)

    def get_bucket_acl(self, bucket_name):
        uri = '%s%s?%s' % (self._fds_base_uri, bucket_name, SubResource.ACL)
        response = requests.get(uri, auth=self._auth)
        if response.status_code == requests.codes.ok:
            acp = AccessControlPolicy(json.loads(response.content))
            acl = self.__acp_to_acl(acp)
            return acl
        else:
            message = 'Get bucket acl failed,status=%s,reason=%s' % (response.status_code, response.content)
            raise GalaxyFDSClientException(message)

    def set_object_acl(self, bucket_name, object_name, acl=None):
        uri = '%s%s/%s?%s' % (self._fds_base_uri, bucket_name, object_name, SubResource.ACL)
        print uri
        acp = self.__acl_to_acp(acl)
        response = requests.put(uri, auth=self._auth, data=json.dumps(acp))
        if response.status_code != requests.codes.ok:
            message = 'Set object acl failed,status=%s,reason=%s' % (response.status_code, response.content)
            raise GalaxyFDSClientException(message)

    def get_object_acl(self, bucket_name, object_name):
        uri = '%s%s/%s?%s' % (self._fds_base_uri, bucket_name, object_name, SubResource.ACL)
        response = requests.get(uri, auth=self._auth)
        if response.status_code == requests.codes.ok:
            acp = AccessControlPolicy.get_access_control_policy(json.loads(response.content))
            acl = self.__acp_to_acl(acp)
            return acl
        else:
            message = 'Get object acl failed,status=%s,reason=%s' % (response.status_code, response.content)
            raise GalaxyFDSClientException(message)

    def get_object_metadata(self, bucket_name, object_name):
        uri = '%s%s/%s?%s' % (self._fds_base_uri, bucket_name, object_name, SubResource.METADATA)
        response = requests.get(uri, auth=self._auth)
        if response.status_code == requests.codes.ok:
            metadata = self.__parse_object_metadata_from_headers(response.headers)
            return metadata
        else:
            message = 'Get object metadata failed,status=%s,reason=%s' % (response.status_code, response.content)
            raise GalaxyFDSClientException(message)

    @staticmethod
    def __acp_to_acl(acp):
        if acp is not None:
            acl = AccessControlList()
            for k in acp['accessControlList']:
                grantee = k['grantee']
                grant_id = grantee['id']
                permission = k['permission']
                g = Grant(Grantee(grant_id), permission)
                acl.add_grant(g)
            return acl
        return ''

    def __acl_to_acp(self, acl):
        if acl is not None:
            acp = AccessControlPolicy()
            owner = Owner()
            owner.id = self._access_key
            acp.owner = owner
            access_control_list = acl.get_grant_list()
            acp.access_control_list = access_control_list
            return acp
        return ''

    @staticmethod
    def __parse_object_metadata_from_headers(response_headers):
        metadata = FDSObjectMetadata()
        header_keys = response_headers.keys()
        for k in FDSObjectMetadata.PRE_DEFINED_METADATA:
            if k in header_keys:
                metadata.add_header(k, response_headers[k])
        for k in response_headers:
            if k.startswith(FDSObjectMetadata.USER_DEFINED_METADATA_PREFIX):
                metadata.add_user_metadata(k, response_headers[k])
        return metadata

        # def getBucketQuota(self, bucket_name):
        # uri = '%s%s?%s' % (self._fds_base_uri, bucket_name, subresource.QUOTA)
        # response = requests.get(uri, auth=self.__auth)
        #   print response.status_code
        #   if response.status_code == requests.codes.ok:
        #     print response.headers

        # def setBucketQuota(self, bucket_name, quota=None):
        #   uri = '%s%s?%s' % (self._fds_base_uri, bucket_name, subresource.QUOTA)
        #   response = requests.put(uri, auth=self.__auth, data=json.dumps(quota))
        #   if response.status_code != requests.codes.ok:
        #     message = 'Set bucket quota failed,status=%s,reason=%s' % (response.status_code, response.content)
        #     raise galaxy_fds_client_exception(message)

