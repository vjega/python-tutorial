# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import (models, 
                       connection)

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

class Activitylog(models.Model):
    activityid = models.BigIntegerField(primary_key=True)
    loginid = models.BigIntegerField()
    pagename = models.CharField(max_length=1000)
    operation = models.CharField(max_length=500)
    usertype = models.IntegerField()
    stringsentence = models.CharField(max_length=2000)
    updateddate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'activitylog'

    @staticmethod
    def recentactivities():
        sql = """SELECT DISTINCT operation,
                    stringsentence,
                    updateddate 
            FROM activitylog al
            INNER JOIN logininfo li ON li.loginid = al.loginid 
            -- WHERE al.loginid = {$loginid} 
            ORDER by activityid DESC 
            LIMIT 5""";
        cursor = connection.cursor()
        cursor.execute(sql)
        return dictfetchall(cursor)

class AdminFolders(models.Model):
    folder_id = models.AutoField(primary_key=True)
    folder_name = models.CharField(max_length=200)
    folder_description = models.CharField(max_length=1000)
    added_date = models.DateTimeField()
    folder_order = models.IntegerField()
    userid = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'admin_folders'

    @staticmethod
    def folders (req):
        sql = """
        SELECT  folder_name,
                folder_id
        FROM admin_folders 
        WHERE userid='%s'
        """%req.user.username 
        # print sql;
        cursor = connection.cursor()
        cursor.execute(sql)
        x = dictfetchall(cursor)
        return x


class AdminResources(models.Model):
    resource_id = models.BigIntegerField(primary_key=True)
    resourcetype = models.CharField(max_length=200)
    resourcetitle = models.CharField(max_length=1000)
    resourcedescription = models.TextField()
    documenturl = models.CharField(max_length=1000)
    imageurl = models.CharField(max_length=1000)
    audiourl = models.CharField(max_length=1000)
    videourl = models.CharField(max_length=1000)
    fileurl = models.CharField(max_length=1000)
    isdeleted = models.IntegerField()
    resource_folder_id = models.IntegerField()
    createdby = models.BigIntegerField()
    createddate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'admin_resources'

class Logininfo(models.Model):
    loginid = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=200, unique=True, db_index=True)
    password = models.CharField(max_length=500)
    firstname = models.CharField(max_length=500)
    lastname = models.CharField(max_length=500)
    isdelete = models.IntegerField()
    lastlogin = models.DateTimeField()
    usertype = models.CharField(max_length=20)
    isadmin = models.IntegerField()
    
    class Meta:
        managed = False
        db_table = 'logininfo'

class Admininfo(models.Model):
    adminid = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=500)
    #username = models.ForeignKey(Logininfo, related_name="username", related_query_name="username")
    password = models.CharField(max_length=500)
    firstname = models.CharField(max_length=500)
    lastname = models.CharField(max_length=500)
    emailid = models.CharField(max_length=500)
    imageurl = models.CharField(max_length=1000)
    isdelete = models.IntegerField()
    createdby = models.BigIntegerField()
    createddate = models.DateTimeField()
    
    class Meta:
        managed = False
        db_table = 'admininfo'


class Assessmentanswerinfo(models.Model):
    assessmentanswerid = models.BigIntegerField(primary_key=True)
    assessmentid = models.BigIntegerField()
    studentid = models.CharField(max_length=500)
    classid = models.BigIntegerField()
    schoolid = models.BigIntegerField()
    answertype = models.CharField(max_length=200)
    assessmentanswer = models.TextField()
    imageurl = models.CharField(max_length=1000)
    audiourl = models.CharField(max_length=1000)
    videourl = models.CharField(max_length=1000)
    rating = models.IntegerField()
    postedby = models.BigIntegerField()
    posteddate = models.DateTimeField()
    isbillboard = models.IntegerField()
    billboardpostedby = models.BigIntegerField()
    billboardposteddate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'assessmentanswerinfo'


class Assessmentanswers(models.Model):
    assessmentanswerid = models.BigIntegerField(primary_key=True)
    assessmentid = models.BigIntegerField()
    questiontype = models.IntegerField()
    questionid = models.BigIntegerField()
    fillinganswer = models.CharField(max_length=1000)
    answer1 = models.IntegerField()
    answer2 = models.IntegerField()
    answer3 = models.IntegerField()
    answer4 = models.IntegerField()
    comprehensionanswer = models.TextField()
    answeredby = models.BigIntegerField()
    answereddate = models.DateTimeField()
    rating = models.IntegerField()
    iscorrect = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'assessmentanswers'


class Assessmentinfo(models.Model):
    assessmentid = models.BigIntegerField(primary_key=True)
    workspaceid = models.BigIntegerField()
    assessmenttitle = models.CharField(max_length=500)
    assessmenttype = models.CharField(max_length=200)
    assessmenttext = models.TextField()
    imageurl = models.CharField(max_length=1000)
    videourl = models.CharField(max_length=1000)
    audiourl = models.CharField(max_length=1000)
    question = models.TextField()
    classid = models.BigIntegerField()
    schoolid = models.BigIntegerField()
    answerformat = models.CharField(max_length=200)
    isstarted = models.IntegerField()
    enddate = models.DateTimeField(blank=True, null=True)
    isended = models.IntegerField()
    postedby = models.BigIntegerField()
    posteddate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'assessmentinfo'


class Assessmentlist(models.Model):
    assessmentid = models.BigIntegerField(primary_key=True)
    assessmenttype = models.IntegerField()
    worktype = models.CharField(max_length=100)
    assessmenttitle = models.CharField(max_length=1000)
    assessmentdescription = models.TextField()
    totalquestions = models.IntegerField()
    totalmarks = models.IntegerField()
    enddate = models.DateTimeField(blank=True, null=True)
    isshared = models.IntegerField()
    ispublished = models.IntegerField()
    isdeleted = models.IntegerField()
    createdby = models.BigIntegerField()
    createddate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'assessmentlist'


class Assignassessmentinfo(models.Model):
    mappingid = models.BigIntegerField(primary_key=True)
    assessmentid = models.BigIntegerField()
    studentid = models.CharField(max_length=500)
    enddate = models.DateTimeField()
    isanswered = models.IntegerField()
    isbillboard = models.IntegerField()
    isclassroom = models.IntegerField()
    assignedby = models.BigIntegerField()
    assigneddate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'assignassessmentinfo'

class Auth_user(models.Model):
    id = models.BigIntegerField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField()
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=75)
    is_staff =models.IntegerField()
    is_active =models.IntegerField()
    date_joined = models.DateTimeField()
    
    class Meta:
        managed = False
        db_table = 'auth_user'


class Assignresourceinfo(models.Model):
    assignedid = models.AutoField(primary_key=True)
    resourceid = models.BigIntegerField()
    studentid = models.CharField(max_length=500)
    assigntext = models.TextField()
    isanswered = models.IntegerField()
    issaved = models.IntegerField()
    originaltext = models.TextField(db_column='originalText')  # Field name made lowercase.
    answertext = models.TextField()
    answerurl = models.CharField(max_length=1000)
    isrecord = models.IntegerField()
    replyformat = models.CharField(max_length=20)
    answerrating = models.IntegerField()
    isbillboard = models.IntegerField()
    isclassroom = models.IntegerField()
    answereddate = models.DateTimeField()
    assignedby = models.CharField(max_length=500)
    assigneddate = models.DateTimeField()
    isdelete = models.IntegerField(db_column='IsDelete')  # Field name made lowercase.
    rubric_id = models.IntegerField()
    rubric_marks = models.CharField(max_length=40)
    rubric_n_mark = models.CharField(max_length=20)
    old_edit = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'assignresourceinfo'


class Assignwrittenworkinfo(models.Model):
    assignwrittenworkid = models.AutoField(primary_key=True)
    writtenworkid = models.BigIntegerField()
    studentid = models.CharField(max_length=500)
    assigntext = models.TextField()
    issaved = models.IntegerField()
    isanswered = models.IntegerField()
    originaltext = models.TextField(db_column='originalText')  # Field name made lowercase.
    answertext = models.TextField(blank=True)
    answerrating = models.IntegerField()
    isbillboard = models.IntegerField()
    isclassroom = models.IntegerField()
    assignedby = models.CharField(max_length=500)
    rubric_id = models.IntegerField()
    assigneddate = models.DateTimeField()
    publisheddate = models.DateTimeField()
    answerurl = models.TextField()
    isrecord = models.IntegerField()
    replyformat = models.CharField(max_length=100)
    answereddate = models.DateTimeField()
    rubric_marks = models.CharField(max_length=100)
    rubric_n_mark = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'assignwrittenworkinfo'


class Billboardinfo(models.Model):
    billboardid = models.BigIntegerField(primary_key=True)
    resourceid = models.BigIntegerField()
    resourcetype = models.CharField(max_length=2)
    studentid = models.CharField(max_length=500)
    votescount = models.IntegerField()
    lastvotedby = models.BigIntegerField()
    lastvoteddate = models.DateTimeField(blank=True, null=True)
    postedby = models.CharField(max_length=500)
    posteddate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'billboardinfo'


class Billboardratinginfo(models.Model):
    billboardratingid = models.BigIntegerField(primary_key=True)
    billboardid = models.BigIntegerField()
    studentid = models.CharField(max_length=500)
    rating = models.BigIntegerField()
    ratedby = models.BigIntegerField()
    rateddate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'billboardratinginfo'


class Billboardvotinginfo(models.Model):
    billboardvotingid = models.BigIntegerField(primary_key=True)
    billboardid = models.BigIntegerField()
    studentid = models.CharField(max_length=500)
    votedby = models.BigIntegerField()
    voteddate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'billboardvotinginfo'


class Bulletinboardinfo(models.Model):
    bulletinboardid = models.AutoField(primary_key=True)
    messagetitle = models.CharField(max_length=1000)
    message = models.CharField(max_length=1000)
    classid = models.BigIntegerField()
    schoolid = models.BigIntegerField()
    attachmenttype = models.CharField(max_length=50)
    isrecord = models.IntegerField()
    attachmenturl = models.CharField(max_length=1000)
    postedby = models.BigIntegerField()
    posteddate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'bulletinboardinfo'

    @staticmethod
    def announcement (req):
        l =  req.user.groups.values_list('name',flat=True)[0]
        fieldcond=""
        joincond=""
        wherecond = ""
        if l == 'Admin' or l == 'Teacher' :
            fieldcond="au.first_name AS postedby"
            joincond="INNER JOIN auth_user au ON au.username = bmi.userid"
            wherecond = "bmi.userid = '%s'"%req.user.username
        else:
            fieldcond="'' AS postedby"
            joincond=""
            wherecond = """bmi.schoolid = '%s'
                           AND bmi.classid = '%s' 
                        """%(req.session.get('stu_schoolid'), 
                             req.session.get('stu_classid'))
        
        sql = """
        SELECT  bbi.bulletinboardid,
                bbi.messagetitle,
                bbi.message,
                %s,
                DATE(bbi.posteddate ) AS posteddate
        FROM bulletinboardinfo bbi
        INNER JOIN bulletinmappinginfo bmi ON bbi.bulletinboardid = bmi.bulletinboardid
        %s
        WHERE %s
        GROUP BY bbi.bulletinboardid
        ORDER by bbi.bulletinboardid DESC
        LIMIT 10"""% (fieldcond,joincond,wherecond)
        cursor = connection.cursor()
        cursor.execute(sql)
        x = dictfetchall(cursor)
        # print x
        return x

class Bulletinmappinginfo(models.Model):
    bulletinmappingid = models.BigIntegerField(primary_key=True)
    bulletinboardid = models.BigIntegerField()
    viewtype = models.IntegerField()
    schoolid = models.BigIntegerField()
    classid = models.BigIntegerField()
    userid = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'bulletinmappinginfo'


class Chapterinfo(models.Model):
    chapterid = models.IntegerField(primary_key=True)
    classid = models.IntegerField()
    sectionid = models.CharField(max_length=3)
    chaptername = models.CharField(max_length=500)
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'chapterinfo'


class Chooseanswerinfo(models.Model):
    chooseanswerid = models.BigIntegerField(primary_key=True)
    choosequestionid = models.BigIntegerField()
    assessmentid = models.BigIntegerField()
    answer = models.TextField()
    iscorrectanswer = models.IntegerField()
    answerorderno = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'chooseanswerinfo'


class Choosequestioninfo(models.Model):
    choosequestionid = models.BigIntegerField(primary_key=True)
    assessmentid = models.BigIntegerField()
    question = models.TextField()
    questiontype = models.CharField(max_length=20)
    questionurl = models.CharField(max_length=1000)
    totalmark = models.IntegerField()
    questionorderno = models.IntegerField()
    isdeleted = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'choosequestioninfo'


class Classinfo(models.Model):
    classid = models.BigIntegerField(primary_key=True)
    classname = models.CharField(max_length=500)
    shortname = models.CharField(max_length=500)
    createdby = models.BigIntegerField()
    createddate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'classinfo'


class Classlessionmappinginfo(models.Model):
    classlessionmappingid = models.BigIntegerField(primary_key=True)
    classid = models.BigIntegerField()
    schoolid = models.BigIntegerField()
    lessionid = models.BigIntegerField()
    createdby = models.BigIntegerField()
    createddate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'classlessionmappinginfo'


class Classroominfo(models.Model):
    classroomid         = models.BigIntegerField(primary_key=True)
    resourceid          = models.BigIntegerField()
    resourcetype        = models.CharField(max_length=2)
    studentid           = models.CharField(max_length=500)
    rating              = models.IntegerField()
    ratingcount         = models.IntegerField()
    votescount          = models.IntegerField()
    lastvotedby         = models.BigIntegerField()
    lastvoteddate       = models.DateTimeField(blank=True, null=True)
    postedby            = models.CharField(max_length=500)
    posteddate          = models.DateTimeField()
    schoolid            = models.BigIntegerField()
    classid             = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'classroominfo'


class Classroomratinginfo(models.Model):
    classroomratingid = models.BigIntegerField(primary_key=True)
    classroomid = models.BigIntegerField()
    studentid = models.CharField(max_length=500)
    rating = models.BigIntegerField()
    ratedby = models.BigIntegerField()
    rateddate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'classroomratinginfo'


class Classroomvotinginfo(models.Model):
    classroomvotingid = models.BigIntegerField(primary_key=True)
    classroomid = models.BigIntegerField()
    studentid = models.CharField(max_length=500)
    votedby = models.BigIntegerField()
    voteddate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'classroomvotinginfo'


class Classschoolmappinginfo(models.Model):
    classschoolmappingid = models.BigIntegerField(primary_key=True)
    classid = models.BigIntegerField()
    schoolid = models.BigIntegerField()
    createdby = models.BigIntegerField()
    createddate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'classschoolmappinginfo'


class Classteachermappinginfo(models.Model):
    classteachermappingid = models.BigIntegerField(primary_key=True)
    schoolid = models.BigIntegerField()
    classid = models.BigIntegerField()
    teacherid = models.BigIntegerField()
    createdby = models.BigIntegerField()
    createddate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'classteachermappinginfo'


class Commentsinfo(models.Model):
    commentid = models.BigIntegerField(primary_key=True)
    billboardid = models.BigIntegerField()
    classroomid = models.BigIntegerField()
    commenttext = models.TextField()
    commentedby = models.BigIntegerField()
    commenteddate = models.DateTimeField()
    isdelete = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'commentsinfo'


class Comprehensioninfo(models.Model):
    comprehensionquestionid = models.BigIntegerField(primary_key=True)
    assessmentid = models.BigIntegerField()
    title = models.TextField()
    description = models.TextField()
    questiontype = models.CharField(max_length=100)
    questionurl = models.CharField(max_length=2000)
    totalmark = models.IntegerField()
    isdeleted = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'comprehensioninfo'


class Coordinatorinfo(models.Model):
    coordinatorid = models.BigIntegerField(primary_key=True)
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    username = models.CharField(max_length=250)
    password = models.CharField(max_length=500)
    emailid = models.CharField(max_length=500)
    dateofbirth = models.DateField()
    gender = models.CharField(max_length=100)
    maritialstatus = models.CharField(max_length=20)
    imageurl = models.CharField(max_length=1000)
    highestqualification = models.CharField(max_length=200)
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=500)
    state = models.CharField(max_length=500)
    country = models.CharField(max_length=500)
    zipcode = models.CharField(max_length=10)
    phonenumber = models.CharField(max_length=20)
    schoolid = models.BigIntegerField()
    createdby = models.BigIntegerField()
    createddate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'coordinatorinfo'


class Editingtext(models.Model):
    editingid = models.BigIntegerField(primary_key=True)
    editid = models.IntegerField()
    spanid = models.CharField(max_length=15)
    previoustext = models.TextField()
    edittext = models.TextField(blank=True)
    editedby = models.CharField(max_length=500)
    editeddate = models.DateTimeField()
    editedplace = models.CharField(max_length=100)
    typeofresource = models.IntegerField()
    usertype = models.IntegerField()
    isapproved = models.IntegerField()
    isrejected = models.IntegerField()
    oritxtrep = models.TextField(db_column='OriTxtRep')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'editingtext'


class Extraslist(models.Model):
    extraid = models.BigIntegerField(primary_key=True)
    extratype = models.CharField(max_length=100)
    resourceurl = models.CharField(max_length=2000)
    classid = models.IntegerField()
    section = models.CharField(max_length=1)
    title = models.TextField()
    description = models.TextField()
    isdeleted = models.IntegerField()
    createddate = models.DateTimeField()
    createdby = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'extraslist'


class Fillingquestionsinfo(models.Model):
    fillingquestionid = models.BigIntegerField(primary_key=True)
    assessmentid = models.BigIntegerField()
    question = models.TextField()
    questiontype = models.CharField(max_length=20)
    actualanswer = models.TextField()
    questionurl = models.CharField(max_length=1000)
    totalmark = models.IntegerField()
    questionorderno = models.IntegerField()
    isdeleted = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'fillingquestionsinfo'


class Foruminfo(models.Model):
    forumid = models.BigIntegerField(primary_key=True)
    forumname = models.CharField(max_length=1000)
    totaltopic = models.IntegerField()
    totalpost = models.IntegerField()
    isdelete = models.IntegerField()
    lastpostedby = models.BigIntegerField()
    lastposteddate = models.DateTimeField()
    createdby = models.BigIntegerField()
    createddate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'foruminfo'


class Lessionassigninfo(models.Model):
    lessionassignid = models.BigIntegerField(primary_key=True)
    lessionid = models.BigIntegerField()
    classid = models.BigIntegerField()
    schoolid = models.BigIntegerField()
    assignedby = models.BigIntegerField()
    assigneddate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'lessionassigninfo'


class Lessioninfo(models.Model):
    lessionid = models.IntegerField(primary_key=True)
    lessiontitle = models.CharField(max_length=500)
    lessiontype = models.CharField(max_length=200)
    imageurl = models.CharField(max_length=1000, blank=True)
    videourl = models.CharField(max_length=1000, blank=True)
    audiourl = models.CharField(max_length=1000, blank=True)
    lessionexplanation = models.TextField(blank=True)
    createdby = models.BigIntegerField()
    createddate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'lessioninfo'


class Lessiontypeinfo(models.Model):
    lessiontypeid = models.IntegerField(primary_key=True)
    originalvalue = models.CharField(max_length=500)
    displayvalue = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = 'lessiontypeinfo'


class Loginhistory(models.Model):
    loginhistoryid = models.BigIntegerField(primary_key=True)
    loginid = models.BigIntegerField()
    logindate = models.DateTimeField()
    loggedoutdate = models.DateTimeField()
    lastvisitedpage = models.CharField(max_length=1000)
    lastvisitedtime = models.DateTimeField()
    isloggedout = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'loginhistory'


class Notesinfo(models.Model):
    notesid = models.BigIntegerField(primary_key=True)
    notestitle = models.CharField(max_length=2000)
    notes = models.TextField()
    isdeleted = models.IntegerField()
    createdby = models.BigIntegerField()
    createddate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'notesinfo'


class Openendedanswerinfo(models.Model):
    openendedanswerid = models.BigIntegerField(primary_key=True)
    openendedquestionid = models.BigIntegerField()
    assessmentid = models.BigIntegerField()
    answer = models.CharField(max_length=2000)
    iscorrectanswer = models.IntegerField()
    answerorderno = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'openendedanswerinfo'


class Openendedquestioninfo(models.Model):
    openendedquestionid = models.BigIntegerField(primary_key=True)
    assessmentid = models.BigIntegerField()
    question = models.TextField()
    studentquestion = models.TextField()
    questiontype = models.CharField(max_length=20)
    questionurl = models.CharField(max_length=2000)
    actualanswer = models.CharField(max_length=2000)
    totalmark = models.IntegerField()
    questionorderno = models.IntegerField()
    isdeleted = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'openendedquestioninfo'


class Pagedetails(models.Model):
    pagedetailid = models.BigIntegerField(primary_key=True)
    pagename = models.CharField(max_length=2000)
    pagedescription = models.CharField(max_length=3000)
    usertype = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'pagedetails'


class PeerRubricsReview(models.Model):
    slno = models.BigIntegerField(primary_key=True)
    resourceid = models.IntegerField()
    studentid = models.IntegerField()
    evaluatedby = models.IntegerField()
    row_no = models.IntegerField()
    row_mark = models.IntegerField()
    max_mark = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'peer_rubrics_review'


class Postinfo(models.Model):
    postid = models.BigIntegerField(primary_key=True)
    topicid = models.BigIntegerField()
    parentid = models.IntegerField()
    forumid = models.BigIntegerField()
    postdetails = models.TextField()
    postedby = models.BigIntegerField()
    posteddate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'postinfo'


class Postreplyinfo(models.Model):
    postreplyid = models.BigIntegerField(primary_key=True)
    postid = models.BigIntegerField()
    postdetails = models.TextField()
    postedby = models.BigIntegerField()
    posteddate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'postreplyinfo'


class Resourceinfo(models.Model):
    resourceid = models.BigIntegerField(primary_key=True)
    categoryid = models.IntegerField()
    classid = models.IntegerField()
    section = models.CharField(max_length=1)
    chapterid = models.IntegerField()
    resourcetype = models.CharField(max_length=200)
    originaltext = models.TextField(db_column='originalText')  # Field name made lowercase.
    resourcetitle = models.CharField(max_length=1000)
    resourcedescription = models.TextField()
    thumbnailurl = models.CharField(max_length=1000)
    documenturl = models.CharField(max_length=1000)
    imageurl = models.CharField(max_length=1000)
    audiourl = models.CharField(max_length=1000)
    videourl = models.CharField(max_length=1000)
    isdeleted = models.IntegerField()
    createdby = models.BigIntegerField()
    createddate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'resourceinfo'


class RubricMatrix(models.Model):
    slno = models.IntegerField(primary_key=True)
    refno = models.IntegerField()
    datatype = models.CharField(max_length=1, blank=True)
    jdata = models.TextField(blank=True)
    disp_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'rubric_matrix'


class RubricsHeader(models.Model):
    slno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    instruction = models.TextField(blank=True)
    teacher = models.CharField(max_length=255)
    status = models.IntegerField()
    ts = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'rubrics_header'


class Schoolinfo(models.Model):
    schoolid = models.BigIntegerField(primary_key=True)
    schoolname = models.CharField(max_length=500)
    shortname = models.CharField(max_length=400)
    description = models.CharField(max_length=1000)
    schoolimageurl = models.CharField(max_length=1000)
    createdby = models.BigIntegerField()
    createddate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'schoolinfo'

class Studentinfo(models.Model):
    studentid = models.BigIntegerField(primary_key=True)
    username = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=50)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    emailid = models.CharField(max_length=100)
    imageurl = models.CharField(max_length=1000)
    schoolid = models.BigIntegerField()
    classid = models.BigIntegerField()
    isdelete = models.IntegerField()
    createdby = models.BigIntegerField()
    createddate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'studentinfo'
        
class Studentworkspaceinfo(models.Model):
    workspaceid = models.BigIntegerField(primary_key=True)
    workspacetitle = models.CharField(max_length=500)
    workspacetype = models.CharField(max_length=200)
    workspacetext = models.TextField()
    documenturl = models.CharField(max_length=1000)
    imageurl = models.CharField(max_length=1000)
    videourl = models.CharField(max_length=1000)
    audiourl = models.CharField(max_length=1000)
    classid = models.BigIntegerField()
    schoolid = models.BigIntegerField()
    isassigned = models.IntegerField()
    isapproved = models.IntegerField()
    isdeleted = models.IntegerField()
    resourceid = models.IntegerField()
    postedby = models.BigIntegerField()
    posteddate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'studentworkspaceinfo'


class TeacherFolders(models.Model):
    folder_id = models.IntegerField(primary_key=True)
    folder_name = models.CharField(max_length=200)
    folder_description = models.CharField(max_length=1000)
    added_date = models.DateTimeField()
    folder_order = models.IntegerField()
    created_by = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'teacher_folders'


class TeacherResources(models.Model):
    resource_id = models.BigIntegerField(primary_key=True)
    resourcetype = models.CharField(max_length=200)
    resourcetitle = models.CharField(max_length=1000)
    resourcedescription = models.TextField()
    documenturl = models.CharField(max_length=1000)
    imageurl = models.CharField(max_length=1000)
    audiourl = models.CharField(max_length=1000)
    videourl = models.CharField(max_length=1000)
    isdeleted = models.IntegerField()
    resource_folder_id = models.IntegerField()
    createdby = models.BigIntegerField()
    createddate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'teacher_resources'


class Teacherinfo(models.Model):
    teacherid = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=500)
    password = models.CharField(max_length=500)
    firstname = models.CharField(max_length=500)
    lastname = models.CharField(max_length=500)
    emailid = models.CharField(max_length=500)
    imageurl = models.CharField(max_length=1000)
    schoolid = models.BigIntegerField()
    classid = models.BigIntegerField()
    isdelete = models.IntegerField()
    createdby = models.BigIntegerField()
    createddate = models.DateTimeField()
    isdelete = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'teacherinfo'

class Teacherresourceinfo(models.Model):
    teacherresourceid = models.BigIntegerField(primary_key=True)
    classid = models.IntegerField()
    section = models.CharField(max_length=1)
    chapterid = models.IntegerField()
    resourcetype = models.CharField(max_length=200)
    resourcecategory = models.IntegerField()
    originaltext = models.TextField(db_column='originalText')  # Field name made lowercase.
    resourcetitle = models.CharField(max_length=1000)
    resourcedescription = models.TextField()
    documenturl = models.CharField(max_length=1000)
    imageurl = models.CharField(max_length=1000)
    audiourl = models.CharField(max_length=1000)
    videourl = models.CharField(max_length=1000)
    schoolid = models.IntegerField()
    isapproved = models.IntegerField()
    isdeleted = models.IntegerField()
    createdby = models.BigIntegerField()
    createddate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'teacherresourceinfo'


class Topicinfo(models.Model):
    topicid = models.BigIntegerField(primary_key=True)
    forumid = models.BigIntegerField()
    topicname = models.CharField(max_length=1000)
    totalpost = models.IntegerField()
    topicdetails = models.TextField()
    lastpostedby = models.BigIntegerField()
    lastposteddate = models.DateTimeField()
    createdby = models.BigIntegerField()
    createddate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'topicinfo'


class Workspaceinfo(models.Model):
    workspaceid = models.BigIntegerField(primary_key=True)
    workspacetitle = models.CharField(max_length=500)
    workspacetype = models.CharField(max_length=200)
    workspacetext = models.TextField()
    documenturl = models.CharField(max_length=1000)
    imageurl = models.CharField(max_length=1000)
    videourl = models.CharField(max_length=1000)
    audiourl = models.CharField(max_length=1000)
    classid = models.BigIntegerField()
    schoolid = models.BigIntegerField()
    isassigned = models.IntegerField()
    isapproved = models.IntegerField()
    isdeleted = models.IntegerField()
    postedby = models.BigIntegerField()
    posteddate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'workspaceinfo'


class Writtenworkinfo(models.Model):
    writtenworkid = models.AutoField(primary_key=True)
    writtenworktitle = models.TextField()
    description = models.TextField()
    writtenimage = models.CharField(db_column='writtenImage', max_length=200)  # Field name made lowercase.
    schoolid = models.IntegerField()
    classid = models.IntegerField()
    isassigned = models.IntegerField()
    createdby = models.CharField(max_length=500)
    isdeleted = models.IntegerField()
    createddate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'writtenworkinfo'

class Calendardetails(models.Model):
    title = models.TextField()
    start = models.DateTimeField()
    end = models.DateTimeField()
    allday = models.BooleanField(default=1)
    color = models.CharField(max_length=30)
    eventcreatedby = models.CharField(max_length=30)
    eventeditedby = models.CharField(max_length=30)
    createdby = models.BigIntegerField()
    isdeleted = models.IntegerField()
    createddate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'calendardetails'

class Mindmap(models.Model):
    title = models.CharField(max_length=200)
    mapdata  = models.TextField()
    createdby = models.BigIntegerField()
    isdelete = models.IntegerField()
    createddate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mindmap'

class stickynotes(models.Model):
    stickylistid = models.BigIntegerField()
    stickytext = models.CharField(max_length=200)
    name  = models.TextField()
    color = models.TextField()
    xyz = models.IntegerField()
    createdby = models.BigIntegerField()
    isdeleted = models.IntegerField()
    createddate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'stickynotes'

class stickycomments(models.Model):
    stickyid = models.IntegerField()
    stickycomment = models.CharField(max_length=200)
    commentby  = models.TextField()
    createdby = models.BigIntegerField()
    isdeleted = models.IntegerField()
    createddate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'stickycomments'

class Threaddetails(models.Model):
    threadid = models.BigIntegerField(primary_key=True)
    topicid = models.BigIntegerField()
    threadname = models.CharField(max_length=1000)
    createdby = models.BigIntegerField()
    createddate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'threaddetails'

class Stickyinfo(models.Model):
    title = models.CharField(max_length=250)
    createdby = models.BigIntegerField()
    isdeleted = models.IntegerField()
    createddate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'stickyinfo'


class Assignmindmapinfo(models.Model):
    assignedid  = models.AutoField(primary_key=True)
    mindmapid   = models.BigIntegerField()
    studentid   = models.CharField(max_length=500)
    assigntext  = models.TextField()
    answertext  = models.TextField()
    mapdata     = models.TextField()
    answereddate= models.DateTimeField()
    assignedby  = models.CharField(max_length=500)
    assigneddate= models.DateTimeField()
    isanswered  = models.IntegerField()
    issaved     = models.IntegerField()
    isdelete    = models.IntegerField(db_column='IsDelete')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table= 'assignmindmapinfo'        