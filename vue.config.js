const {CleanWebpackPlugin} = require('clean-webpack-plugin');
const {WebpackManifestPlugin} = require('webpack-manifest-plugin');

module.exports = {
    css: {
        extract: true
    },
    filenameHashing: false,
    chainWebpack: config => {
        config.plugins.delete('html')
        config.plugins.delete('preload')
        config.plugins.delete('prefetch')
    },
    configureWebpack: {
        plugins: [
            new CleanWebpackPlugin({cleanStaleWebpackAssets: false}),
            new WebpackManifestPlugin({})
        ]
    },

    devServer: {
        port: 8080,
        allowedHosts: [
            '127.0.0.1:8000',
            '127.0.0.1'
        ],
        historyApiFallback: true,
        writeToDisk: true,
        headers: {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, PATCH, OPTIONS',
            'Access-Control-Allow-Headers': 'X-Requested-With, content-type, Authorization'
        }
    },

    runtimeCompiler: true
}