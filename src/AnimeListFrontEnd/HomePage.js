import React, { useState, useEffect } from 'react';
import './HomePage.css';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Navbar = ({ onCategoryChange, onSearch }) => {
    const [searchTerm, setSearchTerm] = useState('');

    const handleSearch = () => {
        console.log("Search clicked with term:", searchTerm);
        onSearch(searchTerm);  
    };

    return (
        <nav>
            <ul className="navbar-list">
                <li>
                    <button onClick={() => onCategoryChange('Main-Page')}>Main Page</button>
                </li>
                <li>
                    <button onClick={() => onCategoryChange('popular')}>Popular</button>
                </li>
                <li className="search-container">
                    <div className="search-wrapper">
                        <input
                            type="text"
                            placeholder="Search"
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                        />
                        <button onClick={handleSearch}>Search</button>
                    </div>
                </li>
                <li>
                    <button onClick={() => onCategoryChange('airing')}>Airing</button>
                </li>
                <li>
                    <button onClick={() => onCategoryChange('most-liked')}>Most Liked</button>
                </li>
                <li>
                    <button onClick={() => onCategoryChange('most-watched')}>Most Watched</button>
                </li>

            </ul>

        </nav>
    );
};




const MovieList = ({ movieData }) => {
    const navigate = useNavigate();
    const handleImageClick = (movie) => {
        navigate('/Content', { state: { movie } });
    };
    return (
        <div className="movie-list">
            {movieData.map((movie, index) => (
                <img key={index} src={movie['large_image_url']} alt={movie['title']}  onClick={() => handleImageClick(movie)}/>
            ))}
        </div>
    );
};
const HomePage = () => {

    const [category, setCategory] = useState('Main-Page');
    const [clicked, setClicked] = useState({}); 
    const [movieData, setMovieData] = useState([]);
    const [pageId, setPageId] = useState(1);
    const [genres, setGenres] = useState([]);


    const fetchMovies = async (ctg) => {

        let currentUrl
        ctg = ctg || category
        if (ctg === 'Main-Page') {
            currentUrl = `/api/animes/${pageId}`
        }
        else {
            currentUrl = `/api/animes/${ctg}/${pageId}`
        }
        try {
            console.log('Fetching movies:', currentUrl);
            const response = await axios.get(currentUrl);
            if (response.status === 200) {
                setMovieData(response.data);
            }
        } catch (error) {
            console.log('Error fetching movies:', error);
        }
    };

    useEffect(() => {
        fetchGenres();
        fetchMovies();
    }, [category, pageId, clicked]);

    const setCategoryFunction = (category) => {
        setCategory(category);
        setClicked({ ...clicked, [category]: true });
        fetchMovies(category);
    }
    const handleSearch = async (searchTerm) => {
        try {
            // Update the URL to include the search term
            const searchUrl = `/api/animes/search/${pageId}`;
            const response = await axios.post(searchUrl, { searchTerm });
            if (response.status === 200) {
                console.log('Search results:', response.data);
                setMovieData(response.data);
            }
        } catch (error) {
            console.error('Error performing search:', error);
        }
    };

    const fetchGenres = async () => {
        try {
            const response = await axios.get('/api/genres/names');
            if (response.status === 200) {
                setGenres(response.data);
            }
        } catch (error) {
            console.error('Error fetching genres:', error);
        }
    };

    const handleGenreClick = async (genre) => {
        try {
            const response = await axios.get(`/api/animes/genre/${genre}/${pageId}`);
            
            if (response.status === 200) {
                setMovieData(response.data);
            }
        } catch (error) {
            console.error('Error making POST request for genre:', error);
        }
    };






    return (
        <div className="home-page">
            <h1 className="h1Style">Welcome to the Home Page!</h1>
            <Navbar onCategoryChange={setCategoryFunction} onSearch={handleSearch} />
            <div className="home-page-content">
                <MovieList movieData={movieData} />
                <div className="yellow-bar">
                    <div className="genre-buttons">
                        {genres.map((genre, index) => (
                            <button key={index} onClick={() => handleGenreClick(genre)}>
                                {genre}
                            </button>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default HomePage;
