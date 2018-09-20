function show(what,e) {
    document.getElementById('shadow').classList.remove('hide');
    e1=document.getElementById(what);
    e1.classList.remove('hide');
    e2=e1.getElementsByTagName("input");
    e2[e2.length-1].setAttribute('id',e.getAttribute('id'));
}

function pull_extrans(e) {
    var row=e.getAttribute('id');
    var table=document.getElementById('dynamic-table');
    document.getElementById('extrans_user').value=table.rows[row].cells[0].innerHTML;
}

function hide(what) {
    document.getElementById('shadow').classList.add('hide');
    document.getElementById(what).classList.add('hide');
    $('.error_msg').text('');
}


function create_id() {
    var e=document.getElementsByClassName("m");
    var num=1;
    for(var i=0;i<e.length;i++) {
        e[i].setAttribute('id',num);
        num+=1
    }
}


function deleteUser(user, ns_list) {
    r = confirm('是否删除用户：' + user + '\n并解绑以下namespace：' + ns_list);
    if(r === true){
        window.open('/delete/'+user,'_self')
    }
}