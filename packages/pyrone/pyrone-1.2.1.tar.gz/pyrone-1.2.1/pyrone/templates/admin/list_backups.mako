<%inherit file="/admin/base.mako"/>

<%def name="title()">${_('Backups')}</%def>

<h2>${_('Backups management')}</h2>

<button class="button" onclick="Pyrone_backup_backupNow('${url('admin_backup_now')}'); return false;"><span class="fa fa-rocket"></span> ${_('Backup blog now')}</button>

<div class="warning" style="display: none;" id="eid-error"></div>
<div class="notify" style="display: none;" id="eid-progress"><span class="fa fa-spin fa-gear"></span> ${_('Restoring backup, please wait')}</div>
<div class="notify" style="display: none;" id="eid-backup-progress"><span class="fa fa-spin fa-gear"></span> ${_('Creating backup, please wait')}</div>

<h3>${_('Backup archives')} 
##<a href="#" class="border-icon">${_('Upload backup file')}</a> 
##<a href="#" class="border-icon" onclick="Pyrone_backup_backupNow('${url('admin_backup_now')}'); return false;">${_('Backup blog now')}</a>
</h3>

<div>${_('Click backup file name to download.')}</div>
<table border="0" class="items-list" cellpadding="0" cellspacing="0" id="backups-table">
<tr>
  <th><input type="checkbox" onclick="Pyrone_selectDeselectAll('backups-table');" id="select-all-files-cb" title="${_('Select/deselect all files')}"/></th>
  <th></th>
  <th>${_('Backup filename')}</th>
  <th>${_('File size')}</th>
</tr>

% for b in backups:
<tr id="list-tr-${b['id']}" data-row-value="${b['filename_b64']}">
  <td><input type="checkbox" value="${b['filename_b64']}" class="list-cb"/></td>
  <td><a href="#" class="border-icon" onclick="Pyrone_backup_startRestoreReq('${url('admin_restore_backup', backup_id=b['filename_b64'])}', 'rb-${b['id']}'); return false;" id="rb-${b['id']}">${_('restore')}</a></td>
  <td><a href="${url('admin_download_backup', backup_id=b['filename_b64'])}" title="${_('Download backup')}">${b['filename']}</a></td>
  <td><span title="${_('{0} bytes').format(b['size'])}">${h.hsize(b['size'])}</span></td>
</tr>
% endfor
</table>

<div>
  <button class="button" onclick="Pyrone_backup_listDeleteSelectedReq('backups-table', '${url('admin_delete_backups_ajax')}'); return false;" id="delete-selected-btn"><span class="fa fa-trash-o"></span> ${_('delete selected')}</button>
</div>