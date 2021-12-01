var picks = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1];

window.onload = function startup() {

    var picks = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1];

    let binary_picks = document.getElementById('binary_picks_data');
    var pick_1 = document.getElementById('pick_1').innerHTML;

    document.getElementById("submit_picks_btn").onclick = function() {
        // check if there are any unpicked teams
        for(var i=0; i<picks.length; i++) {
            if (picks[i] == -1) {
                return;
            }
        }

        var xhr = new XMLHttpRequest();

        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4) {
                if (xhr.response == 'Success'){
                    window.location.replace('/display-competition?id=' + document.getElementById('competition_id').innerHTML)
                }
                else {
                    console.log("error");
                }
            }
        }

        xhr.open("POST", '/make-picks', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(JSON.stringify({
            'picks': picks,
            'competition_id': document.getElementById('competition_id').innerHTML
        }));
    }



    let btn_l_1 = document.getElementById('btn_l_1');
    let btn_r_1 = document.getElementById('btn_r_1');
    btn_l_1.onclick = function() {
        if(btn_r_1.style.backgroundColor == 'rgb(4, 170, 109)' || btn_r_1.style.backgroundColor == '') {
            btn_l_1.style.backgroundColor = 'rgb(4, 170, 109)';
            btn_r_1.style.backgroundColor = '';
        }
        picks[0] = 1;
    }
    btn_r_1.onclick = function() {
        if(btn_l_1.style.backgroundColor == 'rgb(4, 170, 109)' || btn_l_1.style.backgroundColor == '') {
            btn_r_1.style.backgroundColor = 'rgb(4, 170, 109)';
            btn_l_1.style.backgroundColor = '';
        }
        picks[0] = 0;
    }
    if(document.getElementById('pick_1').innerHTML === '1') {
        btn_l_1.style.backgroundColor = 'rgb(4, 170, 109)';
        picks[0] = 1;
    }
    else if (document.getElementById('pick_1').innerHTML === '0') {
        btn_r1.style.backgroundColor = 'rgb(4, 170, 109)';
        picks[0] = 0;
    }

    let btn_l_2 = document.getElementById('btn_l_2');
    let btn_r_2 = document.getElementById('btn_r_2');
    btn_l_2.onclick = function() {
        if(btn_r_2.style.backgroundColor == 'rgb(4, 170, 109)' || btn_r_2.style.backgroundColor == '') {
            btn_l_2.style.backgroundColor = 'rgb(4, 170, 109)';
            btn_r_2.style.backgroundColor = '';
        }
        picks[1] = 1;
    }
    btn_r_2.onclick = function() {
        if(btn_l_2.style.backgroundColor == 'rgb(4, 170, 109)' || btn_l_2.style.backgroundColor == '') {
            btn_r_2.style.backgroundColor = 'rgb(4, 170, 109)';
            btn_l_2.style.backgroundColor = '';
        }
        picks[1] = 0;
    }
    if(document.getElementById('pick_2').innerHTML === '1') {
        btn_l_2.style.backgroundColor = 'rgb(4, 170, 109)';
        picks[1] = 1;
    }
    else if (document.getElementById('pick_2').innerHTML === '0') {
        btn_r_2.style.backgroundColor = 'rgb(4, 170, 109)';
        picks[1] = 0;
    }

    let btn_l_3 = document.getElementById('btn_l_3');
    let btn_r_3 = document.getElementById('btn_r_3');
    btn_l_3.onclick = function() {
        if(btn_r_3.style.backgroundColor == 'rgb(4, 170, 109)' || btn_r_3.style.backgroundColor == '') {
            btn_l_3.style.backgroundColor = 'rgb(4, 170, 109)';
            btn_r_3.style.backgroundColor = '';
        }
        picks[2] = 1;
    }
    btn_r_3.onclick = function() {
        if(btn_l_3.style.backgroundColor == 'rgb(4, 170, 109)' || btn_l_3.style.backgroundColor == '') {
            btn_r_3.style.backgroundColor = 'rgb(4, 170, 109)';
            btn_l_3.style.backgroundColor = '';
        }
        picks[2] = 0;
    }
    if(document.getElementById('pick_3').innerHTML === '1') {
        btn_l_3.style.backgroundColor = 'rgb(4, 170, 109)';
        picks[2] = 1;
    }
    else if (document.getElementById('pick_3').innerHTML === '0') {
        btn_r_3.style.backgroundColor = 'rgb(4, 170, 109)';
        picks[2] = 0;
    }

    let btn_l_4 = document.getElementById('btn_l_4');
    let btn_r_4 = document.getElementById('btn_r_4');
    btn_l_4.onclick = function() {
        if(btn_r_4.style.backgroundColor == 'rgb(4, 170, 109)' || btn_r_4.style.backgroundColor == '') {
            btn_l_4.style.backgroundColor = 'rgb(4, 170, 109)';
            btn_r_4.style.backgroundColor = '';
        }
        picks[3] = 1;
    }
    btn_r_4.onclick = function() {
        if(btn_l_4.style.backgroundColor == 'rgb(4, 170, 109)' || btn_l_4.style.backgroundColor == '') {
            btn_r_4.style.backgroundColor = 'rgb(4, 170, 109)';
            btn_l_4.style.backgroundColor = '';
        }
        picks[3] = 0;
    }
    if(document.getElementById('pick_4').innerHTML === '1') {
        btn_l_4.style.backgroundColor = 'rgb(4, 170, 109)';
        picks[3] = 1;
    }
    else if (document.getElementById('pick_4').innerHTML === '0') {
        btn_r_4.style.backgroundColor = 'rgb(4, 170, 109)';
        picks[3] = 0;
    }

    let btn_l_5 = document.getElementById('btn_l_5');
    let btn_r_5 = document.getElementById('btn_r_5');
    btn_l_5.onclick = function() {
        if(btn_r_5.style.backgroundColor == 'rgb(4, 170, 109)' || btn_r_5.style.backgroundColor == '') {
            btn_l_5.style.backgroundColor = 'rgb(4, 170, 109)';
            btn_r_5.style.backgroundColor = '';
        }
        picks[4] = 1;
    }
    btn_r_5.onclick = function() {
        if(btn_l_5.style.backgroundColor == 'rgb(4, 170, 109)' || btn_l_5.style.backgroundColor == '') {
            btn_r_5.style.backgroundColor = 'rgb(4, 170, 109)';
            btn_l_5.style.backgroundColor = '';
        }
        picks[4] = 0;
    }
    if(document.getElementById('pick_5').innerHTML === '1') {
        btn_l_5.style.backgroundColor = 'rgb(4, 170, 109)';
        picks[4] = 1;
    }
    else if (document.getElementById('pick_5').innerHTML === '0') {
        btn_r_5.style.backgroundColor = 'rgb(4, 170, 109)';
        picks[4] = 0;
    }
    
    let btn_l_6 = document.getElementById('btn_l_6');
    let btn_r_6 = document.getElementById('btn_r_6');
    btn_l_6.onclick = function() {
        if(btn_r_6.style.backgroundColor == 'rgb(4, 170, 109)' || btn_r_6.style.backgroundColor == '') {
            btn_l_6.style.backgroundColor = 'rgb(4, 170, 109)';
            btn_r_6.style.backgroundColor = '';
        }
        picks[5] = 1;
    }
    btn_r_6.onclick = function() {
        if(btn_l_6.style.backgroundColor == 'rgb(4, 170, 109)' || btn_l_6.style.backgroundColor == '') {
            btn_r_6.style.backgroundColor = 'rgb(4, 170, 109)';
            btn_l_6.style.backgroundColor = '';
        }
        picks[5] = 0;
    }
    if(document.getElementById('pick_6').innerHTML === '1') {
        btn_l_6.style.backgroundColor = 'rgb(4, 170, 109)';
        picks[5] = 1;
    }
    else if (document.getElementById('pick_6').innerHTML === '0') {
        btn_r_6.style.backgroundColor = 'rgb(4, 170, 109)';
        picks[5] = 0;
    }
    
    let btn_l_7 = document.getElementById('btn_l_7');
    let btn_r_7 = document.getElementById('btn_r_7');
    btn_l_7.onclick = function() {
        if(btn_r_7.style.backgroundColor == 'rgb(4, 170, 109)' || btn_r_7.style.backgroundColor == '') {
            btn_l_7.style.backgroundColor = 'rgb(4, 170, 109)';
            btn_r_7.style.backgroundColor = '';
        }
        picks[6] = 1;
    }
    btn_r_7.onclick = function() {
        if(btn_l_7.style.backgroundColor == 'rgb(4, 170, 109)' || btn_l_7.style.backgroundColor == '') {
            btn_r_7.style.backgroundColor = 'rgb(4, 170, 109)';
            btn_l_7.style.backgroundColor = '';
        }
        picks[6] = 0;
    }
    if(document.getElementById('pick_7').innerHTML === '1') {
        btn_l_7.style.backgroundColor = 'rgb(4, 170, 109)';
        picks[6] = 1;
    }
    else if (document.getElementById('pick_7').innerHTML === '0') {
        btn_r_7.style.backgroundColor = 'rgb(4, 170, 109)';
        picks[6] = 0;
    }

    let btn_l_8 = document.getElementById('btn_l_8');
    let btn_r_8 = document.getElementById('btn_r_8');
    btn_l_8.onclick = function() {
        if(btn_r_8.style.backgroundColor == 'rgb(4, 170, 109)' || btn_r_8.style.backgroundColor == '') {
            btn_l_8.style.backgroundColor = 'rgb(4, 170, 109)';
            btn_r_8.style.backgroundColor = '';
        }
        picks[7] = 1;
    }
    btn_r_8.onclick = function() {
        if(btn_l_8.style.backgroundColor == 'rgb(4, 170, 109)' || btn_l_8.style.backgroundColor == '') {
            btn_r_8.style.backgroundColor = 'rgb(4, 170, 109)';
            btn_l_8.style.backgroundColor = '';
        }
        picks[7] = 0;
    }
    if(document.getElementById('pick_8').innerHTML === '1') {
        btn_l_8.style.backgroundColor = 'rgb(4, 170, 109)';
        picks[7] = 1;
    }
    else if (document.getElementById('pick_8').innerHTML === '0') {
        btn_r_8.style.backgroundColor = 'rgb(4, 170, 109)';
        picks[7] = 0;
    }

    let btn_l_9 = document.getElementById('btn_l_9');
    let btn_r_9 = document.getElementById('btn_r_9');
    btn_l_9.onclick = function() {
        if(btn_r_9.style.backgroundColor == 'rgb(4, 170, 109)' || btn_r_9.style.backgroundColor == '') {
            btn_l_9.style.backgroundColor = 'rgb(4, 170, 109)';
            btn_r_9.style.backgroundColor = '';
        }
        picks[8] = 1;
    }
    btn_r_9.onclick = function() {
        if(btn_l_9.style.backgroundColor == 'rgb(4, 170, 109)' || btn_l_9.style.backgroundColor == '') {
            btn_r_9.style.backgroundColor = 'rgb(4, 170, 109)';
            btn_l_9.style.backgroundColor = '';
        }
        picks[8] = 0;
    }
    if(document.getElementById('pick_9').innerHTML === '1') {
        btn_l_9.style.backgroundColor = 'rgb(4, 170, 109)';
        picks[8] = 1;
    }
    else if (document.getElementById('pick_9').innerHTML === '0') {
        btn_r_9.style.backgroundColor = 'rgb(4, 170, 109)';
        picks[8] = 0;
    }

    let btn_l_10 = document.getElementById('btn_l_10');
    let btn_r_10 = document.getElementById('btn_r_10');
    btn_l_10.onclick = function() {
        if(btn_r_10.style.backgroundColor == 'rgb(4, 170, 109)' || btn_r_10.style.backgroundColor == '') {
            btn_l_10.style.backgroundColor = 'rgb(4, 170, 109)';
            btn_r_10.style.backgroundColor = '';
        }
        picks[9] = 1;
    }
    btn_r_10.onclick = function() {
        if(btn_l_10.style.backgroundColor == 'rgb(4, 170, 109)' || btn_l_10.style.backgroundColor == '') {
            btn_r_10.style.backgroundColor = 'rgb(4, 170, 109)';
            btn_l_10.style.backgroundColor = '';
        }
        picks[9] = 0;
    }
    if(document.getElementById('pick_10').innerHTML === '1') {
        btn_l_10.style.backgroundColor = 'rgb(4, 170, 109)';
        picks[9] = 1;
    }
    else if (document.getElementById('pick_10').innerHTML === '0') {
        btn_r_10.style.backgroundColor = 'rgb(4, 170, 109)';
        picks[9] = 0;
    }

    let btn_l_11 = document.getElementById('btn_l_11');
    let btn_r_11 = document.getElementById('btn_r_11');
    btn_l_11.onclick = function() {
        if(btn_r_11.style.backgroundColor == 'rgb(4, 170, 109)' || btn_r_11.style.backgroundColor == '') {
            btn_l_11.style.backgroundColor = 'rgb(4, 170, 109)';
            btn_r_11.style.backgroundColor = '';
        }
        picks[10] = 1;
    }
    btn_r_11.onclick = function() {
        if(btn_l_11.style.backgroundColor == 'rgb(4, 170, 109)' || btn_l_11.style.backgroundColor == '') {
            btn_r_11.style.backgroundColor = 'rgb(4, 170, 109)';
            btn_l_11.style.backgroundColor = '';
        }
        picks[10] = 0;
    }
    if(document.getElementById('pick_11').innerHTML === '1') {
        btn_l_11.style.backgroundColor = 'rgb(4, 170, 109)';
        picks[10] = 1;
    }
    else if (document.getElementById('pick_11').innerHTML === '0') {
        btn_r_11.style.backgroundColor = 'rgb(4, 170, 109)';
        picks[10] = 0;
    }

    let btn_l_12 = document.getElementById('btn_l_12');
    let btn_r_12 = document.getElementById('btn_r_12');
    btn_l_12.onclick = function() {
        if(btn_r_12.style.backgroundColor == 'rgb(4, 170, 109)' || btn_r_12.style.backgroundColor == '') {
            btn_l_12.style.backgroundColor = 'rgb(4, 170, 109)';
            btn_r_12.style.backgroundColor = '';
        }
        picks[11] = 1;
    }
    btn_r_12.onclick = function() {
        if(btn_l_12.style.backgroundColor == 'rgb(4, 170, 109)' || btn_l_12.style.backgroundColor == '') {
            btn_r_12.style.backgroundColor = 'rgb(4, 170, 109)';
            btn_l_12.style.backgroundColor = '';
        }
        picks[11] = 0;
    }
    if(document.getElementById('pick_12').innerHTML === '1') {
        btn_l_12.style.backgroundColor = 'rgb(4, 170, 109)';
        picks[11] = 1;
    }
    else if (document.getElementById('pick_12').innerHTML === '0') {
        btn_r_12.style.backgroundColor = 'rgb(4, 170, 109)';
        picks[11] = 0;
    }

    let btn_l_13 = document.getElementById('btn_l_13');
    let btn_r_13 = document.getElementById('btn_r_13');
    btn_l_13.onclick = function() {
        if(btn_r_13.style.backgroundColor == 'rgb(4, 170, 109)' || btn_r_13.style.backgroundColor == '') {
            btn_l_13.style.backgroundColor = 'rgb(4, 170, 109)';
            btn_r_13.style.backgroundColor = '';
        }
        picks[12] = 1;
    }
    btn_r_13.onclick = function() {
        if(btn_l_13.style.backgroundColor == 'rgb(4, 170, 109)' || btn_l_13.style.backgroundColor == '') {
            btn_r_13.style.backgroundColor = 'rgb(4, 170, 109)';
            btn_l_13.style.backgroundColor = '';
        }
        picks[12] = 0;
    }
    if(document.getElementById('pick_13').innerHTML === '1') {
        btn_l_13.style.backgroundColor = 'rgb(4, 170, 109)';
        picks[12] = 1;
    }
    else if (document.getElementById('pick_13').innerHTML === '0') {
        btn_r_13.style.backgroundColor = 'rgb(4, 170, 109)';
        picks[12] = 0;
    }

    let btn_l_14 = document.getElementById('btn_l_14');
    let btn_r_14 = document.getElementById('btn_r_14');
    btn_l_14.onclick = function() {
        if(btn_r_14.style.backgroundColor == 'rgb(4, 170, 109)' || btn_r_14.style.backgroundColor == '') {
            btn_l_14.style.backgroundColor = 'rgb(4, 170, 109)';
            btn_r_14.style.backgroundColor = '';
        }
        picks[13] = 1;
    }
    btn_r_14.onclick = function() {
        if(btn_l_14.style.backgroundColor == 'rgb(4, 170, 109)' || btn_l_14.style.backgroundColor == '') {
            btn_r_14.style.backgroundColor = 'rgb(4, 170, 109)';
            btn_l_14.style.backgroundColor = '';
        }
        picks[13] = 0;
    }
    if(document.getElementById('pick_14').innerHTML === '1') {
        btn_l_14.style.backgroundColor = 'rgb(4, 170, 109)';
        picks[13] = 1;
    }
    else if (document.getElementById('pick_14').innerHTML === '0') {
        btn_r_14.style.backgroundColor = 'rgb(4, 170, 109)';
        picks[13] = 0;
    }

    let btn_l_15 = document.getElementById('btn_l_15');
    let btn_r_15 = document.getElementById('btn_r_15');
    btn_l_15.onclick = function() {
        if(btn_r_15.style.backgroundColor == 'rgb(4, 170, 109)' || btn_r_15.style.backgroundColor == '') {
            btn_l_15.style.backgroundColor = 'rgb(4, 170, 109)';
            btn_r_15.style.backgroundColor = '';
        }
        picks[14] = 1;
    }
    btn_r_15.onclick = function() {
        if(btn_l_15.style.backgroundColor == 'rgb(4, 170, 109)' || btn_l_15.style.backgroundColor == '') {
            btn_r_15.style.backgroundColor = 'rgb(4, 170, 109)';
            btn_l_15.style.backgroundColor = '';
        }
        picks[14] = 0;
    }
    if(document.getElementById('pick_15').innerHTML === '1') {
        btn_l_15.style.backgroundColor = 'rgb(4, 170, 109)';
        picks[14] = 1;
    }
    else if (document.getElementById('pick_15').innerHTML === '0') {
        btn_r_15.style.backgroundColor = 'rgb(4, 170, 109)';
        picks[14] = 0;
    }

    let btn_l_16 = document.getElementById('btn_l_16');
    let btn_r_16 = document.getElementById('btn_r_16');
    btn_l_16.onclick = function() {
        if(btn_r_16.style.backgroundColor == 'rgb(4, 170, 109)' || btn_r_16.style.backgroundColor == '') {
            btn_l_16.style.backgroundColor = 'rgb(4, 170, 109)';
            btn_r_16.style.backgroundColor = '';
        }
        picks[15] = 1;
    }
    btn_r_16.onclick = function() {
        if(btn_l_16.style.backgroundColor == 'rgb(4, 170, 109)' || btn_l_16.style.backgroundColor == '') {
            btn_r_16.style.backgroundColor = 'rgb(4, 170, 109)';
            btn_l_16.style.backgroundColor = '';
        }
        picks[15] = 0;
    }
    if(document.getElementById('pick_16').innerHTML === '1') {
        btn_l_16.style.backgroundColor = 'rgb(4, 170, 109)';
        picks[15] = 1;
    }
    else if (document.getElementById('pick_16').innerHTML === '0') {
        btn_r_16.style.backgroundColor = 'rgb(4, 170, 109)';
        picks[15] = 0;
    }


    
}