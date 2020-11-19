function follow(id){
  fetch(`http://127.0.0.1:8000/follow/${id}`)
  .then(response=>response.json())
  .then(result=>{
    if (document.querySelector(`#follow-btn`).innerText=="Unfollow"){
      document.querySelector(`#follow-btn`).innerHTML="Follow";
    }
    else{
        document.querySelector(`#follow-btn`).innerHTML="Unfollow";
    }
    document.querySelector(`#follower`).innerHTML=result.followers;

  })
  .catch(error=>{
    alert("Something's wrong!");
  });
}
