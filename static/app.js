$(document).ready(function () {

    // immediately upon loading the page, the webiste calls the movie database adn selects a random film

    const filmUrl = "https://api.themoviedb.org/3/movie/550"
    const ranNum = Math.random() * 1100
    const apiKey = "?api_key=98003250cab93815401d6d3944d8a675"


    $.ajax({
        url: filmUrl + ranNum + apiKey,
        content: "application/json",
        dataType: 'json',
        success: function(data) {
            
            // Once the film is summoned, the poster, poster path, film title, plot, and film id are grabbed and displayed on page

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

            $("#pic").append(`<img src="${img}"/>`).val()
            $("#film-title").append(title).val()        
            $("#plot").append(text).val()

            console.log(movie)

            // if the user wants to watch the film, the data is grabbed as JSON and displayed on the following page

            $("#movieForm").append(`<input type='hidden' name='data' value='${JSON.stringify(movie)}' />`);
            
        }
    })
})
