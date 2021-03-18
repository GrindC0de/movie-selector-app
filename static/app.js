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

            const movie = {
                id,
                title : title,
                img : imgPath
            }

            console.log(movie)

            $("#pic").append(`<img src="${img}"/>`).val()
            $("#film-title").append(title).val()        
            $("#plot").append(text).val()

            // need to add values to the form so that the form can post these values to the backend
            $('#movieForm').append(`<input type='hidden' name='data' value='${JSON.stringify(movie)}' />`);
                
        }
    })
})


function rateMovie () {
    const resp = document.getElementById('watch-this').addEventListener('click', function () {
        axios.post('rate-movie')
        console.log(resp)
    })
}

function getNewMovie() {
    window.location.reload();
}