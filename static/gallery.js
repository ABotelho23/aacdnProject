
//Picture Script
  (function() {
    'use strict';
    window.addEventListener('load', function() {
      document.querySelector('#carousel-btn-first').addEventListener('click', function (e) {
        var ev = new CustomEvent('command', {detail: {action: 'first'}});
        document.querySelector('#mdlext-carousel-demo2').dispatchEvent(ev);
      });
      document.querySelector('#carousel-btn-scroll-prev').addEventListener('click', function (e) {
        var ev = new CustomEvent('command', {detail: {action: 'scroll-prev'}});
        document.querySelector('#mdlext-carousel-demo2').dispatchEvent(ev);
      });
      document.querySelector('#carousel-btn-prev').addEventListener('click', function (e) {
        var ev = new CustomEvent('command', {detail: {action: 'prev'}});
        document.querySelector('#mdlext-carousel-demo2').dispatchEvent(ev);
      });
      document.querySelector('#carousel-btn-next').addEventListener('click', function (e) {
        var ev = new CustomEvent('command', {detail: {action: 'next'}});
        document.querySelector('#mdlext-carousel-demo2').dispatchEvent(ev);
      });
      document.querySelector('#carousel-btn-scroll-next').addEventListener('click', function (e) {
        var ev = new CustomEvent('command', {detail: {action: 'scroll-next'}});
        document.querySelector('#mdlext-carousel-demo2').dispatchEvent(ev);
      });
      document.querySelector('#carousel-btn-last').addEventListener('click', function (e) {
        var ev = new CustomEvent('command', {detail: {action: 'last'}});
        document.querySelector('#mdlext-carousel-demo2').dispatchEvent(ev);
      });
      document.querySelector('#carousel-btn-play-pause').addEventListener('click', function (e) {
        // Toggle play icon
        var i = this.querySelector('i');
        var action = i.innerText === 'play_circle_outline' ? 'play' : 'pause';
        i.textContent = action === 'play' ? 'pause_circle_outline' : 'play_circle_outline';
        var ev = new CustomEvent('command', {detail: {action: action, interval: 3000}});
        document.querySelector('#mdlext-carousel-demo2').dispatchEvent(ev);
      });
      document.querySelector('#mdlext-carousel-demo2').addEventListener('select', function (e) {
        if ('pause' === e.detail.command) {
          // Set play icon
          var i = document.querySelector('#carousel-btn-play-pause i');
          i.textContent = 'play_circle_outline';
        }
        else {
          var oldImage = document.querySelector('#carousel-imgviewer img');
          var selectImage = e.detail.source.querySelector('img');
          var selectImageSrc = selectImage.src;
          if (e.detail.source.querySelector('a')) {
            selectImageSrc = e.detail.source.querySelector('a').href;
          }
          if (selectImageSrc !== oldImage.src) {
            var newImage = oldImage.cloneNode(true);
            newImage.src = selectImageSrc;
            oldImage.parentNode.replaceChild(newImage, oldImage);
            var title = document.querySelector('#carousel-viewer-title');
            title.textContent = selectImage.title;
          }
        }
      });
    });
  }());



//Video Script
  (function() {
    'use strict';
    window.addEventListener('load', function() {
      document.querySelector('#carousel-btn-first2').addEventListener('click', function (e) {
        var ev = new CustomEvent('command', {detail: {action: 'first'}});
        document.querySelector('#mdlext-carousel-demo3').dispatchEvent(ev);
      });
      document.querySelector('#carousel-btn-scroll-prev2').addEventListener('click', function (e) {
        var ev = new CustomEvent('command', {detail: {action: 'scroll-prev'}});
        document.querySelector('#mdlext-carousel-demo3').dispatchEvent(ev);
      });
      document.querySelector('#carousel-btn-prev2').addEventListener('click', function (e) {
        var ev = new CustomEvent('command', {detail: {action: 'prev'}});
        document.querySelector('#mdlext-carousel-demo3').dispatchEvent(ev);
      });
      document.querySelector('#carousel-btn-next2').addEventListener('click', function (e) {
        var ev = new CustomEvent('command', {detail: {action: 'next'}});
        document.querySelector('#mdlext-carousel-demo3').dispatchEvent(ev);
      });
      document.querySelector('#carousel-btn-scroll-next2').addEventListener('click', function (e) {
        var ev = new CustomEvent('command', {detail: {action: 'scroll-next'}});
        document.querySelector('#mdlext-carousel-demo3').dispatchEvent(ev);
      });
      document.querySelector('#carousel-btn-last2').addEventListener('click', function (e) {
        var ev = new CustomEvent('command', {detail: {action: 'last'}});
        document.querySelector('#mdlext-carousel-demo3').dispatchEvent(ev);
      });
      document.querySelector('#carousel-btn-play-pause2').addEventListener('click', function (e) {
        // Toggle play icon
        var i = this.querySelector('i');
        var action = i.innerText === 'play_circle_outline' ? 'play' : 'pause';
        i.textContent = action === 'play' ? 'pause_circle_outline' : 'play_circle_outline';
        var ev = new CustomEvent('command', {detail: {action: action, interval: 3000}});
        document.querySelector('#mdlext-carousel-demo3').dispatchEvent(ev);
      });
      document.querySelector('#mdlext-carousel-demo3').addEventListener('select', function (e) {
        if ('pause' === e.detail.command) {
          // Set play icon
          var i = document.querySelector('#carousel-btn-play-pause2 i');
          i.textContent = 'play_circle_outline';
        }
        else {
          var oldImage = document.querySelector('#carousel-imgviewer2 video');
          var selectImage = e.detail.source.querySelector('video');
          var selectImageSrc = selectImage.src;
          if (e.detail.source.querySelector('a')) {
            selectImageSrc = e.detail.source.querySelector('a').href;
          }
          if (selectImageSrc !== oldImage.src) {
            var newImage = oldImage.cloneNode(true);
            newImage.src = selectImageSrc;
            oldImage.parentNode.replaceChild(newImage, oldImage);
            var title = document.querySelector('#carousel-viewer-title2');
            title.textContent = selectImage.title;
          }
        }
      });
    });
  }());
