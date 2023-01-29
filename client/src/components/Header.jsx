import React, { Fragment, useState } from 'react'
import '../styles/css/header.css'
import {ReactComponent as Twitter} from '../assets/svg/twitter.svg'
import { Link } from 'react-router-dom'
import { setJwtToken, setRefreshToken, getJwtToken, getRefreshToken } from '../includes/session'
import { useEffect } from 'react'

const Header = (props) => {
  const [isLogged, setIsLogged] = useState(props.isLogged)
  // check is user is logged in
  const jwtToken = getJwtToken()
  const refTok = getRefreshToken()
  useEffect(()=>{
    if (!jwtToken && !refTok) {
      setIsLogged(false)
    } else {
      setIsLogged(true)
    }
  },[])
  const logout = () => {
    setJwtToken('')
    setRefreshToken('')
    setIsLogged(false)
    window.location.reload();
  }
  return (
    <Fragment>
        <header className="header">
          <div className="header-container">
            <div className="header-brand">
              <div className="twitter-logo">
              <Link to="/"><Twitter className="twitterLogo" /></Link>
              </div>
              <div className="brand-texts">
                <Link to="/"><h3>Twitter Hate Speech Detection</h3></Link>
              </div>
            </div>
            <div className="navigation">
              <nav className="nav">
                <ul className="nav-list">
                  <li className="nav-link">
                    <Link className="nav-red" to="/about">About</Link>
                  </li>
                  <li className="nav-link">
                    <Link className="nav-red" to="/history">History</Link>
                  </li>
                  <li className="nav-link">
                    <Link className="nav-red" to="/contact">Contact</Link>
                  </li>
                  {(!isLogged)?
                    <div style={{display: "flex"}}>
                      <li className="nav-link">
                        <Link className="nav-red auth-btn-login" state="login" to="/auth">Login</Link>
                      </li>
                      <li className="nav-link">
                        <Link className="nav-red auth-btn-register" state="register" to="/auth">Register</Link>
                      </li>
                    </div>:
                      <li className="nav-link">
                        <span style={{cursor: "pointer"}} className="nav-red auth-btn-login" onClick={()=>{logout()}}>logout</span>
                      </li>
                  }
                </ul>
              </nav>
            </div>
          </div>
        </header>
    </Fragment>
  )
}

export default Header