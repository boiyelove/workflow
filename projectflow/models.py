from django.db import models
from teamflow.models import Team, TeamMember
from webcore.models import TimestampedModel

# Create your models here.
JOB_STATUS = (('Todo', 'Todo'),
			('Doing', 'Doing'),
			('Done', 'Done'),)

class JobModel(TimestampedModel):
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=160)
	status = models.CharField(max_length=5, choices=JOB_STATUS)

	class Meta:
		abstract = True


class Project(JobModel):
	pass



class Task(JobModel):
	project = models.ForeignKey(Project)
	team_member = models.ManyToManyField(TeamMember)