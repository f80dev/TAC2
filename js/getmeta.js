
    const metas = document.getElementsByTagName('meta');

    for (let i = 0; i < metas.length; i++) {
        if (metas[i].getAttribute('name') === #1) {
            return metas[i].getAttribute('content');
        }
    }

    return '';
