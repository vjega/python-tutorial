<?php

include '../teachersessions.php';

require "../config.php";

$loginid = $_SESSION['loginid'];
$lastvisitedpage = "newfilling.php";
require "../loggedindetails.php";

updateloginhistory($loginid,$lastvisitedpage);


$selectedclassid = 0;
$classid=0;
$schoolid=0;
$imageurl = "../dbinterface/";
$type = "savewrittenwork";
$assessmentid = 0;

if(isset($_GET['assessmentid']))
{
	$assessmentid = $_GET['assessmentid'];
	
	$type = "savefillingquestion";
}

$myimage = $imageurl . $_SESSION['teacherimage']; 

?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html;  charset=utf-8" />
<title>எழுத்து வேலை</title>
<script type="text/javascript" src="js/jquery.min.js"></script>
<script type="text/javascript" src="js/FormDesign.js"></script>
<script type="text/javascript" src="../ckeditor/ckeditor.js"></script>
<script src="../ckeditor/_samples/sample.js" type="text/javascript"></script>
<link href="../ckeditor/_samples/sample.css" rel="stylesheet" type="text/css" />

<link href="style/sigaram.css" rel="stylesheet" type="text/css" />
<script language="javascript">

function showassigning()
{
	
	url = "assessmentassigninglist.php";
	window.open(url,"wdwSearch","top=100,left=100,width=847,height=300,scrollbars=1,menu=0");
	
}


function addstudentsname(studentid,studentname)
{
	var optn = document.createElement("OPTION");
	optn.text = studentname;
	optn.value = studentid;
	document.resources.stuselectbox.options.add(optn);
	
	document.resources.txtstudents.value = document.resources.txtstudents.value + studentid + ','; 
}


animatedcollapse.addDiv('addstudentsdata', 'fade=1');

animatedcollapse.ontoggle=function($, divobj, state)
{
	//Do Nothing
}

animatedcollapse.init();

function showdiv()
{
	$("div:eq(0)").show("fast", function () 
	  {
		
		$(this).next("addstudentsdata").show("slow", arguments.callee);
	  });

	
	animatedcollapse.toggle('addstudentsdata');
}

function closediv()
{
	//document.getElementById('addstudent').style.display = 'none';
	animatedcollapse.toggle('addstudentsdata');
}

function remstudent()
{
	removeOptions(document.resources.stuselectbox);
}

function removeOptions(selectbox)
{
	var i;
	for(i=selectbox.options.length-1;i>=0;i--)
	{
		if(selectbox.options[i].selected)
		{
			
			removestudent(selectbox.options[i].value);
			selectbox.remove(i);
			
		}
	}
}

function removeall()
{
	if(document.getElementById('chkremoveall').checked)
	{
		var i;
		selectbox = document.resources.stuselectbox;
		for(i=selectbox.options.length-1;i>=0;i--)
		{
				removestudent(selectbox.options[i].value);
				selectbox.remove(i);			
		}
	}	
}


</script>

<script language="javascript">

function removestudent(studentid)
{
			
			if(document.resources.txtstudents.value!="")
			{
				var studentarray=document.resources.txtstudents.value.split(",");
				var studentdataarray = document.resources.studentdata.value.split(",");
				
				if(studentarray.length>0)
				{	
					var matched=0;
					document.resources.txtstudents.value = "";
					for(j=0;j<studentarray.length-1; j++)
					{
						//alert(studentarray.length)
						if(studentarray[j]==studentid)
						{
							matched=1;
						}
						else
						{

							document.resources.txtstudents.value =   document.resources.txtstudents.value  + studentarray[j] + ",";
						}
					}
					
				}
				
				if(studentdataarray.length>0)
				{	
					var matched=0;
					document.resources.studentdata.value = "";
					for(j=0;j<studentdataarray.length-1; j++)
					{
						//alert(studentarray.length)
						if(studentdataarray[j]==studentid)
						{
							
							j = j+2;
							matched=1;
						}
						else
						{
							//alert(studentdataarray[j])
							document.resources.studentdata.value =   document.resources.studentdata.value  + studentdataarray[j] + ",";
							
							
							
						}
					}
					
				}
			}
						
		
	showstudents();
	
}


	function showstudents()
	{
			var studentdataarray=document.resources.studentdata.value.split(",");
			
				var FillDiv="";
				FillDiv = "<table cellpadding='2' class=\"testdesign\">";
					FillDiv = FillDiv + "<tr bgcolor='#318AEE'>";
							FillDiv = FillDiv + "<td>";
								FillDiv = FillDiv + "வ.எண்";							
							FillDiv = FillDiv + "</td>";

							FillDiv = FillDiv + "<td>";
								FillDiv = FillDiv + "முதல் பெயர்";														
							FillDiv = FillDiv + "</td>";
							
							FillDiv = FillDiv + "<td>";
								FillDiv = FillDiv + "கடைசி பெயர்";														
							FillDiv = FillDiv + "</td>";
							
							FillDiv = FillDiv + "<td>";
								FillDiv = FillDiv + "நீக்கு";														
							FillDiv = FillDiv + "</td>";

					FillDiv = FillDiv + "</tr>";
				var count = 1;
				var j=0;
				for (i=0;i<studentdataarray.length-1;i++)
				{
					if(j%2==0)
					{
						FillDiv = FillDiv + "<tr bgcolor='#CCCCCC'>";	
					}
					else
					{
						FillDiv = FillDiv + "<tr bgcolor='#EEEEEE' >";
					}
					
							FillDiv = FillDiv + "<td>";
								//FillDiv = FillDiv + myarray[i];
								FillDiv = FillDiv + count;
							FillDiv = FillDiv + "</td>";
							i=i+1;	
							FillDiv = FillDiv + "<td >";
								FillDiv = FillDiv + studentdataarray[i];
							FillDiv = FillDiv + "</td >";
							i=i+1;	
							FillDiv = FillDiv + "<td >";
								FillDiv = FillDiv + studentdataarray[i];
							FillDiv = FillDiv + "</td>";
							
							FillDiv = FillDiv + "<td >";
								FillDiv = FillDiv + "<img src=\"images/delete.PNG\" style=\"cursor:pointer;\" onclick=\"removestudent('" +  studentdataarray[i-2]  + "');\"  >";
							FillDiv = FillDiv + "</td>";


					FillDiv = FillDiv + "</tr>";			
					j=j+1;
					count++;
				}			
				FillDiv = FillDiv + "</table>";
				//alert(FillDiv)
				document.getElementById('tblstudents').innerHTML=FillDiv;
	}

	function addstudents()
	{
		//var studentarrary=document.resources.txtstudents.value.split(",");
			
		//alert(studentarrary)
		
		if(document.resources.studentslist.length >0)
		{
			
		}
		else
		{
			if(document.resources.txtstudents.value!="")
			{
				var studentarray=document.resources.txtstudents.value.split(",");
				
				if(studentarray.length>0)
				{	
					var matched=0;
					for(j=0;j<studentarray.length; j++)
					{
						
						if(studentarray[j]==document.resources.studentslist.value)
						{
							matched=1;
						}
						else
						{
							//document.resources.txtstudents.value = document.resources.txtstudents.value  + document.resources.studentslist[i].value + ",";
						}
					}
					if(matched == 0)
					{
						
						var optn = document.createElement("OPTION");
						optn.text = document.getElementById('first'+ document.resources.studentslist.value).innerHTML;
						optn.value = document.resources.studentslist.value;
						document.resources.stuselectbox.options.add(optn);
							
						document.resources.txtstudents.value = document.resources.txtstudents.value  + document.resources.studentslist.value + ",";
						//alert(document.getElementById('first'+ document.resources.studentslist[i].value).innerHTML)
						document.resources.studentdata.value = document.resources.studentdata.value  + document.resources.studentslist.value + ",";
						
						document.resources.studentdata.value = document.resources.studentdata.value  + document.getElementById('first'+ document.resources.studentslist.value).innerHTML + ",";
						
						document.resources.studentdata.value = document.resources.studentdata.value  + document.getElementById('last'+ document.resources.studentslist.value).innerHTML + ",";
						
					}
				}
				else
				{
					var optn = document.createElement("OPTION");
					optn.text = document.getElementById('first'+ document.resources.studentslist.value).innerHTML;
					optn.value = document.resources.studentslist.value;
					document.resources.stuselectbox.options.add(optn);
					
					document.resources.txtstudents.value = document.resources.txtstudents.value  + document.resources.studentslist.value + ",";
					
					document.resources.studentdata.value = document.resources.studentdata.value  + document.resources.studentslist.value + ",";
						
					document.resources.studentdata.value = document.resources.studentdata.value  + document.getElementById('first'+ document.resources.studentslist.value).innerHTML + ",";
					
					document.resources.studentdata.value = document.resources.studentdata.value  + document.getElementById('last'+ document.resources.studentslist.value).innerHTML + ",";
				}
		}
		else
		{
			var optn = document.createElement("OPTION");
			optn.text = document.getElementById('first'+ document.resources.studentslist.value).innerHTML;
			optn.value = document.resources.studentslist.value;
			document.resources.stuselectbox.options.add(optn);
			document.resources.txtstudents.value = document.resources.txtstudents.value  + document.resources.studentslist.value + ",";
			
			document.resources.studentdata.value = document.resources.studentdata.value  + document.resources.studentslist.value + ",";
				

			document.resources.studentdata.value = document.resources.studentdata.value  + document.getElementById('first'+ document.resources.studentslist.value).innerHTML + ",";
			
			document.resources.studentdata.value = document.resources.studentdata.value  + document.getElementById('last'+ document.resources.studentslist.value).innerHTML + ",";
		}
		
		}
		
		
		for(var i=0; i<document.resources.studentslist.length; i++)
		{
			
			if(document.resources.studentslist[i].checked)
			{
				if(document.resources.txtstudents.value!="")
				{
					var studentarray=document.resources.txtstudents.value.split(",");
					
					if(studentarray.length>0)
					{	
						var matched=0;
						for(j=0;j<studentarray.length; j++)
						{
							
							if(studentarray[j]==document.resources.studentslist[i].value)
							{
								matched=1;
							}
							else
							{
								//document.resources.txtstudents.value = document.resources.txtstudents.value  + document.resources.studentslist[i].value + ",";
							}
						}
						if(matched == 0)
						{
							var optn = document.createElement("OPTION");
							optn.text = document.getElementById('first'+ document.resources.studentslist[i].value).innerHTML;
							optn.value = document.resources.studentslist[i].value;
							document.resources.stuselectbox.options.add(optn);
							
							document.resources.txtstudents.value = document.resources.txtstudents.value  + document.resources.studentslist[i].value + ",";
							//alert(document.getElementById('first'+ document.resources.studentslist[i].value).innerHTML)
							document.resources.studentdata.value = document.resources.studentdata.value  + document.resources.studentslist[i].value + ",";
							
							document.resources.studentdata.value = document.resources.studentdata.value  + document.getElementById('first'+ document.resources.studentslist[i].value).innerHTML + ",";
							
							document.resources.studentdata.value = document.resources.studentdata.value  + document.getElementById('last'+ document.resources.studentslist[i].value).innerHTML + ",";
							
						}
					}
					else
					{
							var optn = document.createElement("OPTION");
							optn.text = document.getElementById('first'+ document.resources.studentslist[i].value).innerHTML;
							optn.value = document.resources.studentslist[i].value;
							document.resources.stuselectbox.options.add(optn);
							
						
						document.resources.txtstudents.value = document.resources.txtstudents.value  + document.resources.studentslist[i].value + ",";
						
						document.resources.studentdata.value = document.resources.studentdata.value  + document.resources.studentslist[i].value + ",";
							
						document.resources.studentdata.value = document.resources.studentdata.value  + document.getElementById('first'+ document.resources.studentslist[i].value).innerHTML + ",";
						
						document.resources.studentdata.value = document.resources.studentdata.value  + document.getElementById('last'+ document.resources.studentslist[i].value).innerHTML + ",";
					}
				}
				else
				{
							
							var optn = document.createElement("OPTION");
							optn.text = document.getElementById('first'+ document.resources.studentslist[i].value).innerHTML;
							optn.value = document.resources.studentslist[i].value;
							document.resources.stuselectbox.options.add(optn);
							
				
						document.resources.txtstudents.value = document.resources.txtstudents.value  + document.resources.studentslist[i].value + ",";
						
					document.resources.studentdata.value = document.resources.studentdata.value  + document.resources.studentslist[i].value + ",";
							
						document.resources.studentdata.value = document.resources.studentdata.value  + document.getElementById('first'+ document.resources.studentslist[i].value).innerHTML + ",";
						
						document.resources.studentdata.value = document.resources.studentdata.value  + document.getElementById('last'+ document.resources.studentslist[i].value).innerHTML + ",";
						
				}				
			}
		}
		
		showstudents();
	}
	
	function selectallstudents()
	{
		
		
		if(document.resources.selectall.checked)
		{
			if(document.resources.studentslist.length>0)
			{
				
			}
			else
			{
				document.resources.studentslist.checked = true;
			}
			
			for(var i=0; i<document.resources.studentslist.length; i++)
			{
				document.resources.studentslist[i].checked = true;
			}
		}
		else
		{
			if(document.resources.studentslist.length>0)
			{
				
			}
			else
			{
				document.resources.studentslist.checked = false;
			}
			
			for(var i=0; i<document.resources.studentslist.length; i++)
			{
				document.resources.studentslist[i].checked = false;
			}
		}
		
	}
</script>

<script language="javascript">

function getallstudents()
{
	//var f=document.viewproperty;
	var httpxml=getXmlHttpObject();
	
	function getstudents() 
	{
		  if(httpxml.readyState==4)
		  {
				var myarray=eval(httpxml.responseText);
			
				var FillDiv="";
				FillDiv = "<table cellpadding='2'>";
					FillDiv = FillDiv + "<tr bgcolor='#318AEE'>";
							FillDiv = FillDiv + "<td>";
								FillDiv = FillDiv + "<input type='checkbox' name='selectall' id='selectall' onclick=selectallstudents(); \>";							
							FillDiv = FillDiv + "</td>";

							FillDiv = FillDiv + "<td>";
								FillDiv = FillDiv + "முதல் பெயர்";														
							FillDiv = FillDiv + "</td>";
							
							FillDiv = FillDiv + "<td>";
								FillDiv = FillDiv + "கடைசி பெயர்";														
							FillDiv = FillDiv + "</td>";
							

					FillDiv = FillDiv + "</tr>";

				var j=0;
				for (i=0;i<myarray.length;i++)
				{
					if(j%2==0)
					{
						FillDiv = FillDiv + "<tr bgcolor='#CCCCCC'>";	
					}
					else
					{
						FillDiv = FillDiv + "<tr bgcolor='#EEEEEE' >";
					}
					
							FillDiv = FillDiv + "<td>";
								//FillDiv = FillDiv + myarray[i];
								FillDiv = FillDiv + "<input type=\"checkbox\" name=\"studentslist\" id=\"studentslist\" value= "+ myarray[i] + "\>";
							FillDiv = FillDiv + "</td>";
							i=i+1;	
							FillDiv = FillDiv + "<td id=first"+ myarray[i-1] +">";
								FillDiv = FillDiv + myarray[i];
							FillDiv = FillDiv + "</td >";
							i=i+1;	
							FillDiv = FillDiv + "<td id=last"+ myarray[i-2] +">";
								FillDiv = FillDiv + myarray[i];
							FillDiv = FillDiv + "</td>";
							

					FillDiv = FillDiv + "</tr>";			
					j=j+1;
				}			
				FillDiv = FillDiv + "</table>";
				
				document.getElementById('tblselection').innerHTML=FillDiv;
		 }
	}
	
	var url="assigndetails.php";
	url=url+"?type=getallstudents";

	var e = document.getElementById("schools");
	var schoolid = e.options[e.selectedIndex].value;

	var e = document.getElementById("classess");
	var classid = e.options[e.selectedIndex].value;

	url=url+"&schoolid=" + schoolid;
	url=url+"&classid=" + classid;
	
	httpxml.onreadystatechange=getstudents;
	httpxml.open("GET",url,true);
	httpxml.send(null);
}

</script>

<script language="javascript">
	function getclassess()
	{
	 	document.getElementById('tblselection').innerHTML = "";
		
		var httpxml1=getXmlHttpObject();
		function getclass()
		{
			if(httpxml1.readyState==4)
			  {
					var f=document.resources;
			
					var myarray=eval(httpxml1.responseText);
					
					for(j=f.classess.options.length-1;j>=0;j--)
					{
						f.classess.remove(j);
					}
					
					for (i=0;i<myarray.length;i++)
					{
						var optn = document.createElement("OPTION");
						optn.text = myarray[i];
						i=i+1;
						optn.value = myarray[i];
						f.classess.options.add(optn);
					}
					
					//document.getElementById('apDiv3').style.display='none';
			 }
			 
		}
		
		var url="assigndetails.php";
		url=url+"?type=getclassessassignresource";
	
		var e = document.getElementById("schools");
		var schoolid = e.options[e.selectedIndex].value;

		url=url+"&schoolid=" + schoolid; 
		
		httpxml1.onreadystatechange=getclass;
		httpxml1.open("GET",url,true);
		httpxml1.send(null);	
	}
</script>

<script language="javascript">
	function getXmlHttpObject()
{
	  try
	  {
	  	return new XMLHttpRequest();
	  }
	  catch (e)
	  {
		  try
			{
				 return new ActiveXObject("Msxml2.XMLHTTP");
			}
			catch (e)
			{
				try
				{
					return new ActiveXObject("Microsoft.XMLHTTP");
				}
				catch (e)
				{
					alert("Your browser does not support AJAX!");
					return false;
				}
			}
	  }
	  return null;
}
</script>
</head>

<body>
	<div id="containerb">
		<?php include("include/header.php"); ?>
	  <div id="mainbodyp">
	  		
			
	  <div id="mainbodyfull" align="center">
			
			<div class="topleft"><img src="images/topleft.gif" /></div>
				<div class="topright"><img src="images/curveright.gif" /></div>
				<div class="botleft"><img src="images/botleft.gif" /></div>
				<div class="botright"><img src="images/botright.gif" /></div>
				
        <div style="width:900px;" align="left">
        <br />
        <p align="center" class="page_head">எழுத்து வேலை</p>
				<p align="right" class="arrow"><b><a href="writtenwork.php" class="style16"><img src="images/back_button.gif" title="திரும்பிச் செல்" border="0" /></a></b></p>	
<form action="../dbinterface/writtenworkinfo.php" method="post" enctype="multipart/form-data" name="resources" id="resources">
                    <p>
                      <input type="hidden" name="type" id="type" value="<?php echo $type; ?>" />
                      
          </p>
<p class="head_txt">தலைப்பு &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<textarea name="writttenworktitle" cols="50" id="writttenworktitle" style="font-size:14px"></textarea>
                       <script type="text/javascript">
			//<![CDATA[
			CKEDITOR.replace( 'writttenworktitle',
			{
				skin : '<?=CKEDITOR_SKIN?>'
			});
			//]]>
			</script>  
            
		  </p>
          <p class="black_txt">&nbsp;</p>
                    <p class="head_txt">குறிப்பு
<p>
	<textarea name="assigntext" cols="50" id="assigntext" style="font-size:14px"></textarea>
                      <script type="text/javascript">
			//<![CDATA[
			CKEDITOR.replace( 'assigntext',
			{
				skin : '<?=CKEDITOR_SKIN?>'
			});
			//]]>
			</script> 
<p>
                    <input type="file" name="writtenImage" id="writtenImage" />
            <input type="hidden" name="type" value="<?php echo $type; ?>" />
<input type="hidden" name="writtenworkid" value="<?php echo $writtenworkid; ?>" />
          <p>
            <input type="hidden" name="txtstudents" id="txtstudents" />
            <input type="hidden" name="studentdata" id="studentdata" />
</p>
          <p>&nbsp;</p>
          <table width="204" border="0" cellspacing="0" cellpadding="0">
          <tr>
              <td class="head_txt" >Select</td>
            </tr>
            <tr>
              <td width="142" rowspan="2"><select name="stuselectbox" size="10" style="width:150px;" multiple="multiple" id="stuselectbox">
                <option value="0"></option>
                            </select></td>
				<td>&nbsp;&nbsp;</td>
              <td width="62" height="62"><p>
                <input type="button" name="button3" id="button3" value="add"  style="font-size:12px" onclick="showassigning();" class="buttonstlsmall" />
              </p>
              <p>
                <input type="button" name="button4" id="button4" value="remove"  style="font-size:12px" onclick="remstudent();" class="buttonstlsmall"/>
</p></td>
            </tr>
            <tr>
              <td>&nbsp;</td>
            </tr>
          </table>
          
          <div id="addstudentsdata" style="display:none; position:absolute; width: 542px;">
          	<table width="100%" class="testdesign" border="0" cellspacing="0" cellpadding="0">
            <tr>
              <td width="41%"><select name="schools" id="schools" onchange="getclassess();">
                  <option value="0">All</option>
                  <?php 
					$q=mysql_query("SELECT schoolid, schoolname FROM `schoolinfo` ");
				
					$i=0;
					while($nt=mysql_fetch_array($q))
					{
					?>
                  <option value="<?=$nt['schoolid']; ?>">
                    <?=$nt['schoolname'] ?>
                  </option>
                  <?php 
					}
					?>
                </select>              </td>
              <td width="28%"><select name="classess" id="classess" onchange="">
                  <option value="0">All</option>
              </select></td>
              <td><input type="button" name="button5" id="button5" value="எடு" class="buttonstlsmall" onclick="getallstudents();" />
              <input type="button" name="button2" id="button2" value="சேர்" class="buttonstlsmall" onclick="addstudents();" />
              
              <img src="images/close.gif" onclick="closediv();" style="cursor:pointer;" />              </td>
            </tr>
            <tr>
              <td colspan="3"><div id="tblselection" style="height:200px;overflow:auto;"> </div></td>
            </tr>
          </table>
          
          </div>
          
          <p>          
          <p>
          <div id="tblstudents" style="height:200px;overflow:auto;font-size:14px;display:none;">
            	
    </div>
  </p>
  
          <p>&nbsp;</p>
<p>
                      <input type="submit" name="button" id="button" value="சேமிக்கவும்" class="buttonstl" /> &nbsp; <input type="submit" name="send" id="send" value="அனுப்பவும்" class="buttonstl" />
		  </p>
          </form>
<p>
 				       
			      </p>
 				    <div >
                    
                      
                        
	      </div>
		    <p>&nbsp;</p>
        </div>
                
                
				
	  </div>
	  
	  </div>
	</div>
</body>
</html>
