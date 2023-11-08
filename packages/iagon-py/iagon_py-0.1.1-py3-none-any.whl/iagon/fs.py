# # class PathInfo(BaseModel):

# #     @classmethod
# #     def from_iagon(cls, response: Dict[str, Optional[str]], is_dir=False):
# #         return PathInfo(


# class IagonFS(AsyncFileSystem):
#     """Access Iagon as if it were a file system.

#     This exposes Iagon as a filesystem-like API.

#     Use the API storage key to gain access.

#     Reliant on S3FileSystem as a template.

#     https://github.com/fsspec/s3fs/blob/main/s3fs/core.py

#     Args:
#     """

#     def __init__(self, token=None):
#         if token is None:

#     async def _ls(self, path: str, detail: bool = True):

#         ).json()["data"]["directories"]


#         if len(directories) == 0:

#         for directory in directories:
#         for file in files:
#             if "parent_directory_id" in file and file["parent_directory_id"] in ids:

#         if detail:

#     async def _mkdir(self, path: str, create_parents=True):

#         if create_parents:
#             for i in range(1, len(parents) - 1):

#     def _open(self, path, mode="rb"):


# class IagonFile(AbstractBufferedFile):
#     """Open Iagon file.


#     Args:
#     """
