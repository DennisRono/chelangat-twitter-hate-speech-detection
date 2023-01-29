import React, { Fragment } from 'react'
import '../styles/css/about.css'
import Header from '../components/Header'
import { Helmet } from "react-helmet"
import { ReactComponent as Send } from '../assets/svg/arrow-up-right-from-square.svg'

const About = () => {
  return (
    <Fragment>
        <Helmet>
            <meta charSet="utf-8" />
            <title>About | Twitter Hate Speech Detection</title>
        </Helmet>
        <Header/>
        <div className="about">
            <h1 className="about-title">Twitter hate crime and cyberbullying detection</h1>
            <p className="creator">Created by <a href="https://github.com/zarina" rel="noopener noreferrer" target="_blank">Cynthia Chelang'at <Send className="sendicon"/></a></p>
            <p className="abt-cont">This project aims to <strong>automate content moderation</strong> to identify hate speech using <strong>machine learning binary classification algorithms.</strong></p>
            <p className="abt-cont">Baseline models included Random Forest, Naive Bayes, Logistic Regression and Support Vector Machine (SVM). The final model was a <strong>Logistic Regression</strong> model that used Count Vectorization for feature engineering. It produced an F1 of 0.3958 and Recall (TPR) of 0.624.</p>
            <h2>The problem of content moderation</h2>
            <p className="abt-cont"><strong>Human content moderation exploits people by consistently traumatizing and underpaying them.</strong> In 2019, an <a href="https://www.theverge.com/2019/6/19/18681845/facebook-moderator-interviews-video-trauma-ptsd-cognizant-tampa" target="_blank" rel="noopener noreferrer">article</a> on The Verge exposed the extensive list of horrific working conditions that employees faced at Cognizant, which was Facebook’s primary moderation contractor. Unfortunately, <strong>every major tech company</strong>, including <strong>Twitter</strong>, uses human moderators to some extent, both domestically and overseas.</p>
        </div>
    </Fragment>
  )
}

export default About