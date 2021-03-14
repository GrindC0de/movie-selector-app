$(document).ready(function () {
    const filmUrl = "https://api.themoviedb.org/3/movie/550"
    const ranNum = Math.random() * 900
    const apiKey = "?api_key=98003250cab93815401d6d3944d8a675"


    $.ajax({
        url: filmUrl + ranNum + apiKey,
        content: "application/json",
        dataType: 'json',
        success: function(data) {
            
            const imgPath = `${data.poster_path}`
            const img = `https://image.tmdb.org/t/p/w500/${data.poster_path}`
            const title = `${data.title}`
            const text = `${data.overview}`
            const id = `${data.id}`

            const imgObj = JSON.stringify(imgPath)
            const titleObj = JSON.stringify(title)
            const textObj = JSON.stringify(text)

            const poster = $("#pic").append(`<img src="${img}"/>`)
            const resTitle = $("#film-title").append(titleObj)        
            const resText = $("#plot").append(textObj)

            console.log(resTitle, resText, poster, id)
            
            window.localStorage.setItem

        }
    })
})


function rateMovie() {

    window.onload = function (data) { 
        document.querySelector('#watch-this').addEventListener('click', function() {
            const title = $('#film-title').val(data)
            const img = $('#pic').val(data) 
            localStorage.setItem('rate-film', title, img)
            console.log(rateFilm)
        });
    }
}

function getNewMovie() {
    window.location.reload();
}