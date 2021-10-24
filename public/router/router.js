import { constants } from '../consts/consts';
import {
  pathParamRegExp,
  pathPropTypeRegexp,
  regSubstr,
  urlRegexp,
} from '../consts/regexp';

/**
 * Router
 */
class Router {
  /**
   * Makes new router
   */
  constructor() {
    this.routes = new Map();
  }

  /**
   * Register new view, associated with specific path
   * @param {String} path in string templates format
   * @param {View} view
   * @return {Router}
   */
  register(path, view) {
    this.routes.set(path, view);
    return this;
  }

  /**
   * Goes to specified path
   * @param {String} path
   */
  go(path) {
    if (path.endsWith('/') && path !== '/') {
      path = path.slice(0, -1);
    }

    if (path === '/home') {
      path = '/';
    }

    // const prevView = this.currentView;
    // if (prevView) {
    //   prevView.remove();
    // }

    const key = [...this.routes.keys()].find((key) => key === path);

    this.currentView = this.routes.get(key);

    if (window.location.pathname !== path) {
      window.history.pushState(null, null, path);
    }

    this.currentView.show();
  }

  /**
   * Goes to the previous path
   */
  back() {
    window.history.back();
  }

  /**
   * Goes to the next path
   */
  forward() {
    window.history.forward();
  }

  /**
   * Starts routing
   */
  start() {
    window.addEventListener('popstate', () => this.go('/'));
    window.addEventListener('click', (event) => {
      let targetURL = '';
      if (event.target instanceof HTMLAnchorElement) {
        targetURL = event.target.href;
      } else {
        const parentAnchor = event.target.closest('a');
        if (parentAnchor) {
          targetURL = parentAnchor.href;
        }
      }

      if (targetURL.startsWith(window.location.origin)) {
        event.preventDefault();
        this.go(targetURL.replace(urlRegexp, ''));
      }
    });

    this.go(window.location.pathname);
  }
}

export const appRouter = new Router();
