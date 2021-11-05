var data_file = document.currentScript.getAttribute('data_file');

$(document).ready(function(){
    var music_div = `
    <div class="all-albums">
    `
    $.getJSON(data_file, function(json) {

        var albums = Object.values(json)
        albums.sort((a,b) => (a.rank > b.rank) ? 1 : ((b.rank > a.rank) ? -1 : 0))

        $.each(albums, function(title, values){
            var album_div = 
            `
        <div class="all-album__container">
            <a href="https://open.spotify.com/album/${values.album_uri.split("spotify:album:")[1]}" target="_blank" class="album__item">
                <img src="${values.cover_img}" alt="" class="portfolio__img">
            <div class="album_overlay">
                <div class="album-text">
                    <p class="artist" style="font-size: 10px">Amount of times played: ${values.played}</p>
                    <p class="artist" style="font-size: 10px">Hours played: ${Math.round((values.msPlayed * 0.001)/3600)}</p>
                </div>
            </div>
            </a>
        </div>
            `
        music_div = music_div + album_div
});

        music_div = music_div + `
        </div>
        `
        $('#albums').append(music_div)

    });

});