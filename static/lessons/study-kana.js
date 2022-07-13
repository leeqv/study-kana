import { sideNavHandler } from "./modules/components-nav.js";
import { getSectionName } from "./modules/helpers-others.js";
import { quizHandler } from "./modules/handler-quiz.js";
import { profileHandler } from "./modules/handler-profile.js";
import { studyMenuHandler, reviewMenuHandler, watchlistMenuHandler } from "./modules/handlers-menu.js";
import { oldLessonHandler, newLessonHandler, endOfLessonHandler } from "./modules/handlers-lesson.js";
import { aboutPageHandler } from "./modules/handler-about.js";

var studyKana = {};
(function() {
    this.sectionHandlers = {
        // subsections
        studyMenu: studyMenuHandler,
        reviewMenu: reviewMenuHandler,
        oldLesson: oldLessonHandler,
        newLesson: newLessonHandler,
        endOfLesson: endOfLessonHandler,
        // sections
        about: aboutPageHandler,
        watchlist: watchlistMenuHandler,
        profile: profileHandler,
        quiz: quizHandler,
    };
}).apply(studyKana);

window.addEventListener('load', function(){
    var pathname = window.location.pathname;
    var subsection = {
        [/\/(review)\/[HK]-[\d]+\/[\w]+(\/)?/.test(pathname)]: 'oldLesson',
        [/\/(study)\/[HK]-[\d]+\/[\w]+(\/)?/.test(pathname)]: 'newLesson',
        [/\/(study)\/[HK]-[\d]+\/fin(\/)?/.test(pathname)]: 'endOfLesson',
        [/^\/(study)+(\/)?$/.test(pathname)]: 'studyMenu',
        [/^\/(review)+(\/)?$/.test(pathname)]: 'reviewMenu',
    }
    var methodHandler = studyKana.sectionHandlers[subsection[true] || getSectionName()];
    if (methodHandler) methodHandler();

    // if side nav exists in the page (when user is authenticated)
    if (document.getElementById('toggle-nav')) sideNavHandler();
});