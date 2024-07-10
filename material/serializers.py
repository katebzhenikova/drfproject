from rest_framework import serializers

from material.models import Course, Lessons


class LessonsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lessons
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonsSerializer(read_only=True, many=True)

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    class Meta:
        model = Course
        fields = '__all__'


class CourseCreateSerializer(serializers.ModelSerializer):
    lessons = LessonsSerializer(many=True)

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






