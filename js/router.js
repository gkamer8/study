// Simple hash-based router

export class Router {
    constructor() {
        this.routes = {};
        this.currentRoute = null;
        
        window.addEventListener('hashchange', () => this.handleRoute());
        window.addEventListener('load', () => this.handleRoute());
    }

    on(path, handler) {
        this.routes[path] = handler;
    }

    handleRoute() {
        const hash = window.location.hash.slice(1) || '/';
        const [path, ...paramParts] = hash.split('/').filter(p => p);
        const routePath = '/' + (path || '');
        const params = paramParts;

        let handler = this.routes[routePath];
        
        // Try to find a parameterized route
        if (!handler) {
            for (const [route, h] of Object.entries(this.routes)) {
                if (route.includes(':')) {
                    const routeParts = route.split('/').filter(p => p);
                    const hashParts = ['', path, ...paramParts];
                    
                    if (routeParts.length === hashParts.length - 1) {
                        const namedParams = {};
                        let match = true;
                        
                        for (let i = 0; i < routeParts.length; i++) {
                            if (routeParts[i].startsWith(':')) {
                                namedParams[routeParts[i].slice(1)] = hashParts[i + 1];
                            } else if (routeParts[i] !== hashParts[i + 1]) {
                                match = false;
                                break;
                            }
                        }
                        
                        if (match) {
                            handler = h;
                            return handler(namedParams);
                        }
                    }
                }
            }
        }

        if (handler) {
            this.currentRoute = routePath;
            handler(params.length > 0 ? { params } : {});
        } else {
            console.warn('No handler for route:', hash);
        }
    }

    navigate(path) {
        window.location.hash = path;
    }
}
