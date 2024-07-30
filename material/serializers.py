from rest_framework import serializers
from material.models import Course, Lessons, Subscription
from material.validators import NoExternalLinksValidator


class LessonsSerializer(serializers.ModelSerializer):
    title = serializers.CharField(validators=[NoExternalLinksValidator()])
    video_url = serializers.URLField(validators=[NoExternalLinksValidator()], required=False, allow_blank=True)

    class Meta:
        model = Lessons
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonsSerializer(read_only=True, many=True)
    description = serializers.CharField(validators=[NoExternalLinksValidator()])
    is_subscribed = serializers.SerializerMethodField()

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    class Meta:
        model = Course
        fields = '__all__'

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return Subscription.objects.filter(user=user, course=obj).exists()


class CourseCreateSerializer(serializers.ModelSerializer):
    lessons = LessonsSerializer(many=True)
    description = serializers.CharField(validators=[NoExternalLinksValidator()])

    class Meta:
        model = Course
        fields = '__all__'

    def create(self, validated_data):
        lessons_data = validated_data.pop('lessons')
        course_item = Course.objects.create(**validated_data)

        for lesson_data in lessons_data:
            lesson_data.pop('course', None)

            Lessons.objects.create(course=course_item, **lesson_data)

        return course_item










