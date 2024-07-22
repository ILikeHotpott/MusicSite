import os
from openai import OpenAI
import markdown
from rest_framework.views import APIView
from rest_framework.response import Response

from react_app.throttle import UserRateThrottle, IPRateThrottle


class ChatbotView(APIView):

    def post(self, request):
        content = request.data.get("content")
        if content is None:
            return Response({'error': 'Content parameter is missing'}, status=400)

        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user",
                 "content": f"{content}"}
            ]
        )

        response_content = completion.choices[0].message.content
        html = markdown.markdown(response_content)

        print(html)

        return Response(html)
