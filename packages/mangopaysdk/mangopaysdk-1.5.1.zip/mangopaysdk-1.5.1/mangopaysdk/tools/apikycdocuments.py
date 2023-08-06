from mangopaysdk.tools.apibase import ApiBase

class ApiKycDocuments(ApiBase):
    """MangoPay API for KYC documents."""

    def GetAll(self, pagination = None, sorting = None):
        """Gets all KYC documents.
        param Pagination pagination Pagination object.
        param Sorting sorting Sorting object.
        return Array of objects returned from API
        """
        return self._getList('kyc_documents_all', pagination, 'KycDocument', None, None, sorting)
    