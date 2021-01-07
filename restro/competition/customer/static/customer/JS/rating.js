const thank = document.querySelector(".thank")
const rate = document.querySelector(".widgit")
const back = document.querySelector(".return")

rate.onclick = ()=>
{
    
    rate.style.display = "none";
    thank.style.display = "block";
}

back.onclick = ()=>
{
    thank.style.display = "none";
    rate.style.display = "block";
}

// -------------------------------------

const word = document.querySelector(".content")
const rate1 = document.querySelector(".widgit1")
const exit = document.querySelector(".exit")



rate1.onclick = ()=>
{
    rate1.style.display = "none";
    word.style.display = "block";
}

exit.onclick = ()=>
{
    word.style.display = "none";
    rate1.style.display = "block";
}


var rating="";
function starmark(item)
{
    var count = item.id[0];
    rating = count;
    var subid = item.id.substring(1);
    for (var i=0; i<5; i++)
    {
        if (i<count)
        {
            document.getElementById((i+1)+subid);
        }

        else
        {
            document.getElementById((i+1)+subid);
        }
    }

}


