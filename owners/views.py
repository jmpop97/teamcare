from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from owners.models import PetOwner
from owners.serializers import PetOwnerSerializer, PetOwnerCreateSerializer


# 게시글 목록과 작성
class PetOwnerView(APIView):
    def get(self, request):
        """게시글 목록 불러오기"""
        owner_list = PetOwner.objects.all() # 모든 게시글
        serializer = PetOwnerSerializer(owner_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = PetOwnerCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(writer=request.user)
            return Response({'message':'게시글 작성되었습니다.'}, serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'message':'잘못된 입력 값입니다.'}, serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

# 게시글 상세페이지 수정, 삭제    
class PetOwnerDetailView(APIView):
    def get(self, request, owner_id):
        """게시글 상세보기"""
        owner_post = PetOwner.objects.get(id=owner_id)
        serializer = PetOwnerSerializer(owner_post)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, owner_id):
        """게시글 수정"""
        owner_post = PetOwner.objects.get(id=owner_id)
        if request.user == owner_post.writer:  # 본인이 작성한 게시글이 맞다면
            serializer = PetOwnerCreateSerializer(owner_post, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message':'게시글이 수정 되었습니다.'}, serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'message':'잘못된 입력 값입니다.'}, serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:   # 본인의 게시글이 아니라면
            return Response({'message':'권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
    
    def delete(self, request, owner_id):
        """게시글 삭제"""
        owner_post = PetOwner.objects.get(id=owner_id)
        if request.user == owner_post.writer:  # 본인이 작성한 게시글이 맞다면
            owner_post.delete() 
            return Response({'message':'게시글이 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)
        else:   # 본인의 게시글이 아니라면
            return Response({'message':'권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
'''
# owner_id가 맞나? user/writer랑 헷갈린다
class PetOwnerCommentView(APIView):
    def get(self, request, owner_id):
        # 댓글 요청 함수
        owner = PetOwner.objects.get(id=owner_id)
        comments = owner.owner_set.all()
        serializer = PetOwnerCommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, owner_id):
        # 댓글 작성 함수
        serializer = PetOwnerCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, owner_id=owner_id)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PetOwnerCommentDetailView(APIView):
    def put(self, request, owner_id, comment_id):
        # 댓글 수정 함수
        comment = get_object_or_404(PetOwnerComment, id=comment_id)
        if request.user == comment.user:
            serializer = PetOwnerCommentSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, owner_id, comment_id):
        # 댓글 삭제 함수
        comment = get_object_or_404(PetOwnerComment, id=comment_id)
        if request.user == comment.user:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)

# PetOwnerCommentSerializer 변형한 PetOwnerCommentCreateSerializer 만들어야할지 (js연결할때 확인을 해야하나?)
# Postman으로 테스트시 Header에 적어놔야함
'''
