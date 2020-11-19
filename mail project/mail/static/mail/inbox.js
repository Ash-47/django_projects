document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);


  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#view-mail').style.display = 'none';
  //history.pushState({compose: compose}, "", "compose");
  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
  document.querySelector('#compose-form').addEventListener('submit',(event)=>{
  event.preventDefault();
  let status;
  fetch('/emails', {
  method: 'POST',
  body: JSON.stringify({
      recipients: document.querySelector('#compose-recipients').value,
      subject: document.querySelector('#compose-subject').value,
      body:document.querySelector('#compose-body').value
  })
})
.then((response) => {
  status=response.status;
  return response.json()})
    .then((result) => {
      //console.log(result);
      if(status==201){
        load_mailbox('sent');
      }
      else{
        alert(result.error);
      }

    })
    .catch((error) => {
      console.log('Error:', error);
    });
});
}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#view-mail').style.display = 'none';

  // Show the mailbox name
  history.pushState({mail: mailbox}, "");

  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  if (mailbox=='inbox'){
    showInbox();
  }
  else if(mailbox=='sent'){
    showSent();
  }
  else{
    showArchive();
  }
}


function showInbox(){
  fetch('/emails/inbox')
  .then(response => response.json())
  .then(emails => {
    // Print emails
      var div=document.createElement('div');
      div.innerHTML=`<div class="list-group">`;
    emails.forEach((email, i) => {

    //  console.log(i);
      div.innerHTML+=`<a href="javascript: viewmail(${email.id})"  class="list-group-item list-group-item-action" id="item${i}">
       <div class="d-flex w-100 justify-content-start">
       <p class="mb-0"><strong>${email.sender}</strong></p>
      <p class="mb-0 ml-3">${email.subject}</p>
            </div>
         <div class="d-flex w-100 justify-content-end mb-0">
        <small>${email.timestamp}</small>
        </div>
    </a>`;
     if(email.read){
      div.querySelector(`#item${i}`).style.backgroundColor='#e9ecef';
     }

    });
    div.innerHTML+=`</div>`;

    document.querySelector('#emails-view').appendChild(div);

    // ... do something else with emails ...
  });
}


function showSent(){
  fetch('/emails/sent')
  .then(response => response.json())
  .then(emails => {
    // Print emails
      var div=document.createElement('div');
      div.innerHTML=`<div class="list-group">`;
    emails.forEach((email, i) => {

    //  console.log(emails);
      div.innerHTML+=`<a href="javascript: viewmail(${email.id},1)" class="list-group-item list-group-item-action">
       <div class="d-flex w-100 justify-content-start">
       <p class="mb-0">To: <strong> ${email.recipients}</strong></p>
      <p class="mb-0 ml-3">${email.subject}</p>
            </div>
         <div class="d-flex w-100 justify-content-end mb-0">
        <small>${email.timestamp}</small>
        </div>

    </a>`;

    });
    div.innerHTML+=`</div>`;
    document.querySelector('#emails-view').appendChild(div);

    // ... do something else with emails ...
  });
}

function showArchive(){
  fetch('/emails/archive')
  .then(response => response.json())
  .then(emails => {
    // Print emails
      var div=document.createElement('div');
      div.innerHTML=`<div class="list-group">`;
    emails.forEach((email, i) => {

    //  console.log(emails);
      div.innerHTML+=`<a href="javascript: viewmail(${email.id})" class="list-group-item list-group-item-action">
       <div class="d-flex w-100 justify-content-start">
       <p class="mb-0"> <strong> ${email.sender}</strong></p>
      <p class="mb-0 ml-3">${email.subject}</p>
            </div>
         <div class="d-flex w-100 justify-content-end mb-0">
        <small>${email.timestamp}</small>
        </div>

    </a>`;

    });
    div.innerHTML+=`</div>`;
    document.querySelector('#emails-view').appendChild(div);
    // ... do something else with emails ...
  });
}


function viewmail(email_id,flag=0){
  document.querySelector('#emails-view').style.display='none';
  document.querySelector('#compose-view').style.display='none';
  document.querySelector('#view-mail').style.display='block';
  //console.log(flag);
  fetch(`/emails/${email_id}`)
  .then(response=>response.json())
  .then(result=>{
    const parent=document.querySelector('#view-mail');
  //  console.log(result);
    parent.innerHTML=`<p><strong>From: </strong>${result.sender}</p>
    <p><strong>To: </strong>${result.recipients}</p>
    <p><strong>Subject: </strong>${result.subject}</p>
    <p><strong>Timestamp: </strong>${result.timestamp}</p>
    <button class="btn btn-sm btn-outline-primary" id="reply">Reply</button>
    <button class="btn btn-sm btn-outline-primary" id="archive">Archive</button>
    <hr>
    <p><strong>Body: </strong>${result.body}</p></br> `;
    if(flag){ document.querySelector('#archive').style.display='none';}
    if(result.archived){
      document.querySelector('#archive').innerHTML='Unarchive';
    }

    fetch(`emails/${email_id}`, {
    method: "PUT",
    body: JSON.stringify({
      read: true,
    })});
    document.querySelector('#reply').addEventListener("click",()=>reply(result));
    document.querySelector('#archive').addEventListener("click",()=> archived(result.id,result.archived));

  });
}
function reply(result){
  compose_email();
  if (!/^Re:/.test(result.subject))
  {
    document.querySelector('#compose-subject').value= `Re: ${result.subject}`;}
  else{
      document.querySelector('#compose-subject').value=result.subject;
  }
  document.querySelector('#compose-recipients').value=result.sender;
 document.querySelector("#compose-body").value = `On ${result.timestamp} ${result.sender} wrote:\n${result.body}\n`;
}


function archived(id,state){
  fetch(`/emails/${id}`, {
    method: "PUT",
    body: JSON.stringify({
      archived: !state,
    }),
  });
  load_mailbox('inbox');
}


window.onpopstate = function(event) {
  //  console.log(event.state);
load_mailbox(event.state.mail);
}
