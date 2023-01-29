import React, { Fragment, useState, useEffect } from 'react'
import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router-dom"
import Home from './routes/Home'
import Contact from './routes/Contact'
import About from './routes/About'
import Auth from './routes/Auth'
import History from './routes/History'
import NotFound from './routes/NotFound'
import { getJwtToken, getRefreshToken, setJwtToken } from './includes/session'
import { api } from './api/axios'

const App = () => {
    const [isLogged, setIsLogged] = useState(false)
    // check is user is logged in
    const jwtToken = getJwtToken()
    const refTok = getRefreshToken()
    useEffect(()=>{
      const vToken = async (t, refT) => {
        let ver =  await api('POST', 'auth/verifytoken', {token: t, refreshToken: getRefreshToken()})
        console.log(ver);
        if(ver.type==='error'){
          setIsLogged(false)
        } else {
          setIsLogged(true)
          if(ver.state==='renewed'){
            setJwtToken(ver.token)
          }
        }
      }
      if (!jwtToken && !refTok) {
        setIsLogged(false)
      } else {
        vToken(jwtToken)
      }
    }, [])
  return (
    <Fragment>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Home islogged={isLogged} />} />
            <Route path="/contact" element={<Contact />} />
            <Route path="/about" element={<About />} />
            <Route path="/history" element={<History islogged={isLogged} />} />
            <Route path="/auth" element={<Auth />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </BrowserRouter>
    </Fragment>
  )
}

export default App