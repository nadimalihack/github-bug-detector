/**
 * OAuth Diagnostic Script
 * Paste this in browser console (F12) to diagnose OAuth issues
 */

console.log('🔍 Starting OAuth Diagnostics...\n');

// 1. Check current URL
console.log('1️⃣ Current URL:');
console.log('   ', window.location.href);
const params = new URLSearchParams(window.location.search);
const code = params.get('code');
if (code) {
    console.log('   ✅ OAuth code present:', code.substring(0, 10) + '...');
} else {
    console.log('   ℹ️ No OAuth code in URL');
}
console.log('');

// 2. Check localStorage
console.log('2️⃣ Auth Storage (localStorage):');
const authStorage = localStorage.getItem('auth-storage');
if (authStorage) {
    try {
        const parsed = JSON.parse(authStorage);
        console.log('   Raw:', authStorage.substring(0, 100) + '...');
        console.log('   Parsed:', parsed);
        console.log('   isAuthenticated:', parsed.state?.isAuthenticated);
        console.log('   user:', parsed.state?.user?.login || 'N/A');

        if (parsed.state?.isAuthenticated) {
            console.log('   ✅ User IS authenticated');
        } else {
            console.log('   ❌ User is NOT authenticated');
        }
    } catch (e) {
        console.log('   ❌ Error parsing:', e.message);
    }
} else {
    console.log('   ❌ No auth storage found');
}
console.log('');

// 3. Check sessionStorage
console.log('3️⃣ Session Storage:');
const oauthProcessing = sessionStorage.getItem('oauth_processing');
console.log('   oauth_processing:', oauthProcessing || 'not set');
if (oauthProcessing) {
    console.log('   ⚠️ OAuth processing flag is STUCK - this might cause issues');
    console.log('   Run: sessionStorage.clear() to fix');
}
console.log('');

// 4. Test backend
console.log('4️⃣ Testing Backend:');
fetch('http://localhost:8000/')
    .then(res => res.json())
    .then(data => {
        console.log('   ✅ Backend is running');
        console.log('   Features:', data.features);
    })
    .catch(err => {
        console.log('   ❌ Backend not accessible:', err.message);
    });

// 5. Check what view should be shown
console.log('');
console.log('5️⃣ Expected View:');
if (authStorage) {
    try {
        const parsed = JSON.parse(authStorage);
        if (parsed.state?.isAuthenticated) {
            console.log('   📊 Should show: DASHBOARD');
        } else {
            console.log('   🏠 Should show: CLASSIC VIEW or LOGIN PAGE');
        }
    } catch (e) {
        console.log('   ❓ Unknown (parse error)');
    }
} else {
    console.log('   🏠 Should show: CLASSIC VIEW');
}

console.log('');
console.log('═══════════════════════════════════════════════════');
console.log('📋 RECOMMENDATIONS:');
console.log('═══════════════════════════════════════════════════');

// Recommendations
const recommendations = [];

if (!authStorage) {
    recommendations.push('❌ No auth data - OAuth might have failed');
    recommendations.push('   Try: Clear storage and login again');
}

if (oauthProcessing) {
    recommendations.push('⚠️ OAuth processing flag stuck');
    recommendations.push('   Run: sessionStorage.clear()');
}

if (authStorage) {
    try {
        const parsed = JSON.parse(authStorage);
        if (!parsed.state?.isAuthenticated) {
            recommendations.push('❌ Auth data exists but isAuthenticated is false');
            recommendations.push('   Try: localStorage.clear() and login again');
        } else if (parsed.state?.isAuthenticated) {
            recommendations.push('✅ Auth looks good!');
            recommendations.push('   If not seeing dashboard, try: location.reload()');
        }
    } catch (e) {
        recommendations.push('❌ Auth data is corrupted');
        recommendations.push('   Run: localStorage.clear()');
    }
}

if (recommendations.length === 0) {
    recommendations.push('✅ Everything looks good!');
}

recommendations.forEach(rec => console.log(rec));

console.log('');
console.log('═══════════════════════════════════════════════════');
console.log('🔧 QUICK FIXES:');
console.log('═══════════════════════════════════════════════════');
console.log('// Clear everything and start fresh:');
console.log('localStorage.clear(); sessionStorage.clear(); location.reload();');
console.log('');
console.log('// Just clear session (if stuck):');
console.log('sessionStorage.clear(); location.reload();');
console.log('');
console.log('// Force reload:');
console.log('location.reload(true);');
console.log('═══════════════════════════════════════════════════');
