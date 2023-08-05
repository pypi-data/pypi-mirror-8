/*jsl:declare Ext*/
/*jsl:declare N_*/

/**
 * A single item designated for upload.
 *
 * It is a simple object wrapping the native file API object.
 */
Ext.define('MP.upload.Item', {
    mixins : {
        observable : 'Ext.util.Observable'
    },

    STATUS_READY : N_('ready'),
    STATUS_UPLOADING : N_('uploading'),
    STATUS_UPLOADED : N_('uploaded'),
    STATUS_UPLOAD_ERROR : N_('uploaderror'),

    config : {
        /**
         * @cfg {Object} fileApiObject (required)
         *
         * A native file API object
         */
        fileApiObject : null,

        /**
         * @cfg {String}
         *
         * The upload error message associated with this file object
         */
        uploadErrorMessage : ''
    },

    constructor : function(config) {
        this.mixins.observable.constructor.call(this);

        this.addEvents({
            changestatus : true,
            progressupdate : true
        });

        this.initConfig(config);

        Ext.apply(this, {
            status : this.STATUS_READY,
            progress : 0
        });
    },

    reset : function() {
        this.uploadErrorMessage = '';
        this.setStatus(this.STATUS_READY);
        this.setProgress(0);
    },

    getFileApiObject : function() {
        return this.fileApiObject;
    },

    getId : function() {
        return this.getFilename();
    },

    getFilename : function() {
        return this.getProperty('name');
    },

    getSize : function() {
        return this.getProperty('size');
    },

    getContentType : function() {
        return this.getProperty('type');
    },

    getProperty : function(propertyName) {
        if (this.fileApiObject) {
            return this.fileApiObject[propertyName];
        }

        return null;
    },

    getProgress : function() {
        return this.progress;
    },

    getProgressPercent : function() {
        var progress = this.getProgress();
        if (!progress) {
            return 0;
        }

        var percent = (progress / this.getSize()) * 100;
        if (percent > 100) {
            percent = 100;
        }

        return Ext.util.Format.number(percent, '0');
    },

    setProgress : function(progress) {
        this.progress = progress;
        this.fireEvent('progressupdate', this);
    },

    getStatus : function() {
        return this.status;
    },

    setStatus : function(status) {
        this.status = status;
        this.fireEvent('changestatus', this, status);
    },

    isReady : function() {
        return (this.status == this.STATUS_READY);
    },

    isUploaded : function() {
        return (this.status == this.STATUS_UPLOADED);
    },

    setUploaded : function() {
        this.setProgress(this.getSize());
        this.setStatus(this.STATUS_UPLOADED);
    },

    isUploadError : function() {
        return (this.status == this.STATUS_UPLOAD_ERROR);
    },

    getUploadErrorMessage : function() {
        return this.uploadErrorMessage;
    },

    setUploadError : function(message) {
        this.uploadErrorMessage = message;
        this.setStatus(this.STATUS_UPLOAD_ERROR);
    },

    setUploading : function() {
        this.setStatus(this.STATUS_UPLOADING);
    }
});
